"""
IBM Granite AI client.

Communicates with IBM watsonx text/chat endpoint and returns raw text.
All credentials are read from environment variables – never hardcoded.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config (loaded from environment / .env)
# ---------------------------------------------------------------------------
WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "")
WATSONX_URL: str = os.getenv(
    "WATSONX_URL",
    "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29",
)
WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
GRANITE_MODEL_ID: str = os.getenv("GRANITE_MODEL_ID", "ibm/granite-4-h-small")

IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

# Cache the IAM token in-process (simple TTL-free cache; token lasts ~1 hour)
_cached_token: Optional[str] = None


async def _get_iam_token() -> str:
    """Exchange the IBM Cloud API key for a short-lived IAM bearer token."""
    global _cached_token
    if _cached_token:
        return _cached_token

    if not WATSONX_API_KEY:
        raise RuntimeError(
            "WATSONX_API_KEY is not set. "
            "Copy .env.example → .env and fill in your credentials."
        )

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            IAM_TOKEN_URL,
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": WATSONX_API_KEY,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        _cached_token = resp.json()["access_token"]
        return _cached_token


def invalidate_token() -> None:
    """Force re-authentication on the next request (call after 401)."""
    global _cached_token
    _cached_token = None


async def granite_chat(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """
    Send a chat request to IBM Granite and return the assistant's text reply.

    Raises:
        RuntimeError: when credentials are missing or the API returns an error.
    """
    token = await _get_iam_token()

    payload: Dict[str, Any] = {
        "model_id": GRANITE_MODEL_ID,
        "project_id": WATSONX_PROJECT_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(WATSONX_URL, json=payload, headers=headers)

        # If token expired, refresh once and retry
        if resp.status_code == 401:
            invalidate_token()
            token = await _get_iam_token()
            headers["Authorization"] = f"Bearer {token}"
            resp = await client.post(WATSONX_URL, json=payload, headers=headers)

        if resp.status_code != 200:
            logger.error("Granite API error %s: %s", resp.status_code, resp.text)
            raise RuntimeError(
                f"IBM Granite returned HTTP {resp.status_code}. "
                "Check your credentials and project ID."
            )

        data = resp.json()
        # watsonx chat endpoint returns choices[0].message.content
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            logger.error("Unexpected Granite response shape: %s", data)
            raise RuntimeError("Unexpected response format from IBM Granite.") from exc


async def granite_json(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 1024,
) -> Dict[str, Any]:
    """
    Request a JSON-structured response from Granite and parse it.
    Falls back gracefully if Granite wraps the JSON in markdown fences.
    """
    raw = await granite_chat(system_prompt, user_message, max_tokens=max_tokens, temperature=0.3)

    # Strip markdown code fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        cleaned = "\n".join(inner).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract the first {...} or [...] block
        start = cleaned.find("{")
        if start == -1:
            start = cleaned.find("[")
        if start != -1:
            # Find matching closing bracket
            bracket = "{" if cleaned[start] == "{" else "["
            end_bracket = "}" if bracket == "{" else "]"
            depth = 0
            for i, ch in enumerate(cleaned[start:], start):
                if ch == bracket:
                    depth += 1
                elif ch == end_bracket:
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(cleaned[start : i + 1])
                        except json.JSONDecodeError:
                            break
        raise RuntimeError(
            "IBM Granite did not return valid JSON. Raw response: " + raw[:200]
        )
