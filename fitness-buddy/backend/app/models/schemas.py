"""
Shared Pydantic models used across the application.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# User Profile
# ---------------------------------------------------------------------------
class UserProfile(BaseModel):
    name: str = Field(default="Friend", max_length=50)
    age: Optional[int] = Field(default=None, ge=10, le=120)
    fitness_goal: str = Field(default="general fitness")
    experience_level: str = Field(default="beginner")          # beginner / intermediate / advanced
    workout_duration_minutes: int = Field(default=30, ge=5, le=180)
    equipment: str = Field(default="none")                     # none / dumbbells / bands / gym
    dietary_preference: str = Field(default="balanced")        # balanced / vegetarian / vegan / keto
    activity_level: str = Field(default="sedentary")           # sedentary / light / moderate / active


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    profile: Optional[UserProfile] = None


class ChatResponse(BaseModel):
    reply: str
    type: str = "chat"


# ---------------------------------------------------------------------------
# Workout
# ---------------------------------------------------------------------------
class WorkoutExercise(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    rest_seconds: Optional[int] = None
    instructions: str


class WorkoutRequest(BaseModel):
    profile: Optional[UserProfile] = None
    override_duration: Optional[int] = None
    override_equipment: Optional[str] = None


class WorkoutResponse(BaseModel):
    type: str = "workout"
    title: str
    summary: str
    difficulty: str
    warm_up: List[WorkoutExercise]
    exercises: List[WorkoutExercise]
    cool_down: List[WorkoutExercise]
    safety_note: str


# ---------------------------------------------------------------------------
# Nutrition
# ---------------------------------------------------------------------------
class NutritionRequest(BaseModel):
    profile: Optional[UserProfile] = None
    meal_type: str = Field(default="any")   # breakfast / lunch / dinner / snack / any


class MealSuggestion(BaseModel):
    name: str
    ingredients: List[str]
    preparation: str
    nutritional_highlights: Optional[str] = None
    dietary_tags: List[str] = []


class NutritionResponse(BaseModel):
    type: str = "nutrition"
    meal_type: str
    suggestions: List[MealSuggestion]
    disclaimer: str = (
        "These are general wellness suggestions only and are not medical or dietary advice. "
        "Consult a registered dietitian for personalised guidance."
    )


# ---------------------------------------------------------------------------
# Habits
# ---------------------------------------------------------------------------
class Habit(BaseModel):
    id: str
    label: str
    emoji: str
    completed: bool = False


class HabitUpdateRequest(BaseModel):
    completed: bool


class MotivationResponse(BaseModel):
    quote: str
    tip: str
