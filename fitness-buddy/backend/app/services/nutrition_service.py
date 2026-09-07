"""
Nutrition service – orchestrates Granite calls and validation.
"""
from __future__ import annotations

import logging
from typing import Optional

from app.ai import granite, prompts
from app.ai.schemas import parse_nutrition
from app.models.schemas import UserProfile, NutritionResponse

logger = logging.getLogger(__name__)

_FALLBACK_NUTRITION = NutritionResponse(
    meal_type="any",
    suggestions=[
        {
            "name": "Greek Yoghurt Parfait",
            "ingredients": ["Greek yoghurt", "mixed berries", "granola", "honey"],
            "preparation": "Layer yoghurt, berries, and granola in a glass. Drizzle honey on top.",
            "nutritional_highlights": "High protein, antioxidants, probiotics.",
            "dietary_tags": ["vegetarian", "high-protein"],
        },
        {
            "name": "Veggie Stir-Fry with Brown Rice",
            "ingredients": ["brown rice", "broccoli", "bell pepper", "carrot", "soy sauce", "garlic"],
            "preparation": "Cook rice. Stir-fry vegetables in a little oil with garlic and soy sauce for 5-7 minutes.",
            "nutritional_highlights": "High fibre, vitamins, complex carbohydrates.",
            "dietary_tags": ["vegan", "high-fibre"],
        },
    ],
)


async def get_nutrition(
    profile: Optional[UserProfile] = None,
    meal_type: str = "any",
) -> NutritionResponse:
    """Generate personalised meal suggestions via IBM Granite."""
    system = prompts.nutrition_system_prompt(profile)
    user_msg = (
        f"Suggest 2-3 healthy {meal_type} meal ideas"
        f"{' for a ' + profile.dietary_preference + ' diet' if profile else ''}."
    )

    try:
        raw = await granite.granite_json(system, user_msg, max_tokens=900)
        result = parse_nutrition(raw)
        result.meal_type = meal_type
        return result
    except Exception as exc:
        logger.warning("Nutrition generation failed, using fallback: %s", exc)
        fallback = _FALLBACK_NUTRITION.model_copy()
        fallback.meal_type = meal_type
        return fallback
