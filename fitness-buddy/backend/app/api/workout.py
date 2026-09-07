"""
Workout API – generate personalised workouts via IBM Granite.
"""
from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import WorkoutRequest, WorkoutResponse
from app.services.workout_service import generate_workout

router = APIRouter(tags=["workout"])
logger = logging.getLogger(__name__)


@router.post("/workout", response_model=WorkoutResponse)
async def get_workout(request: WorkoutRequest):
    """Generate a personalised workout plan using IBM Granite."""
    try:
        return await generate_workout(
            profile=request.profile,
            override_duration=request.override_duration,
            override_equipment=request.override_equipment,
        )
    except Exception as exc:
        logger.error("Workout error: %s", exc)
        raise HTTPException(status_code=503, detail="Could not generate workout. Please try again.")
