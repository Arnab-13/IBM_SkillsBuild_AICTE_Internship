"""
Habits API – provide default habits catalogue and motivation.
Client-side localStorage handles persistence.
"""
from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, HTTPException
from app.models.schemas import Habit, MotivationResponse
from app.services.habit_service import get_default_habits
from app.ai import granite, prompts
from app.ai.schemas import parse_motivation

router = APIRouter(tags=["habits"])
logger = logging.getLogger(__name__)


@router.get("/habits", response_model=List[Habit])
async def list_habits():
    """Return the default habit catalogue."""
    return get_default_habits()


@router.get("/motivation", response_model=MotivationResponse)
async def get_motivation():
    """Get a daily motivational quote and wellness tip from IBM Granite."""
    system = prompts.motivation_system_prompt()
    user_msg = "Give me today's motivation and a practical wellness tip."
    try:
        raw = await granite.granite_json(system, user_msg, max_tokens=256)
        return parse_motivation(raw)
    except Exception as exc:
        logger.warning("Motivation failed: %s", exc)
        return MotivationResponse(
            quote="Every rep, every step, every choice – it all adds up. Keep going!",
            tip="Start your day with a 5-minute stretch to boost energy and flexibility.",
        )
