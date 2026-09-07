"""
Habit service – default habit definitions.
State is stored in browser localStorage; this service just provides the catalogue.
"""
from __future__ import annotations

from typing import List
from app.models.schemas import Habit

DEFAULT_HABITS: List[Habit] = [
    Habit(id="workout", label="Complete workout", emoji="💪"),
    Habit(id="water", label="Drink 8 glasses of water", emoji="💧"),
    Habit(id="movement", label="10 min daily movement", emoji="🚶"),
    Habit(id="healthy_meal", label="Eat a healthy meal", emoji="🥗"),
    Habit(id="sleep", label="7-8 hours of sleep", emoji="😴"),
]


def get_default_habits() -> List[Habit]:
    return [h.model_copy() for h in DEFAULT_HABITS]
