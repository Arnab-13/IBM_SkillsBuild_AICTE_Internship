"""
Pydantic validators for raw AI JSON responses.
Keeps validation logic separate from the API layer.
"""
from __future__ import annotations

from typing import Any, Dict

from pydantic import ValidationError

from app.models.schemas import WorkoutResponse, NutritionResponse, MotivationResponse


def parse_workout(data: Dict[str, Any]) -> WorkoutResponse:
    """Validate and return a WorkoutResponse; raises ValueError on bad data."""
    try:
        return WorkoutResponse(**data)
    except (ValidationError, TypeError) as exc:
        raise ValueError(f"Invalid workout data from AI: {exc}") from exc


def parse_nutrition(data: Dict[str, Any]) -> NutritionResponse:
    """Validate and return a NutritionResponse; raises ValueError on bad data."""
    try:
        return NutritionResponse(**data)
    except (ValidationError, TypeError) as exc:
        raise ValueError(f"Invalid nutrition data from AI: {exc}") from exc


def parse_motivation(data: Dict[str, Any]) -> MotivationResponse:
    """Validate and return a MotivationResponse; raises ValueError on bad data."""
    try:
        return MotivationResponse(**data)
    except (ValidationError, TypeError) as exc:
        raise ValueError(f"Invalid motivation data from AI: {exc}") from exc
