"""
Nutrition API – suggest healthy meals via IBM Granite.
"""
from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import NutritionRequest, NutritionResponse
from app.services.nutrition_service import get_nutrition

router = APIRouter(tags=["nutrition"])
logger = logging.getLogger(__name__)


@router.post("/nutrition", response_model=NutritionResponse)
async def nutrition(request: NutritionRequest):
    """Get personalised meal suggestions from IBM Granite."""
    try:
        return await get_nutrition(profile=request.profile, meal_type=request.meal_type)
    except Exception as exc:
        logger.error("Nutrition error: %s", exc)
        raise HTTPException(status_code=503, detail="Could not generate nutrition suggestions. Please try again.")
