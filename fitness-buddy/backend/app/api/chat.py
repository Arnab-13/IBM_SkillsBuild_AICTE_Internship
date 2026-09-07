"""
Chat API – free-form AI conversation with IBM Granite.
"""
from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.ai import granite, prompts

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a free-form message to IBM Granite and receive a conversational reply."""
    system = prompts.chat_system_prompt(request.profile)
    try:
        reply = await granite.granite_chat(system, request.message, max_tokens=512)
        return ChatResponse(reply=reply)
    except RuntimeError as exc:
        logger.error("Chat error: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc))
