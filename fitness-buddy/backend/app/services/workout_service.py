"""
Workout service – orchestrates Granite calls and validation.
"""
from __future__ import annotations

import logging
from typing import Optional

from app.ai import granite, prompts
from app.ai.schemas import parse_workout
from app.models.schemas import UserProfile, WorkoutResponse

logger = logging.getLogger(__name__)

# Fallback workout used when Granite is unavailable
_FALLBACK_WORKOUT = WorkoutResponse(
    title="Quick Bodyweight Workout",
    summary="A simple bodyweight routine you can do anywhere with no equipment.",
    difficulty="beginner",
    warm_up=[
        {
            "name": "Arm Circles",
            "duration_seconds": 30,
            "instructions": "Stand with feet shoulder-width apart. Rotate arms in large circles, 15 seconds forward, 15 seconds backward.",
        },
        {
            "name": "Leg Swings",
            "duration_seconds": 30,
            "instructions": "Hold a wall for balance. Swing each leg forward and back 10 times.",
        },
    ],
    exercises=[
        {
            "name": "Bodyweight Squat",
            "sets": 3,
            "reps": 12,
            "rest_seconds": 30,
            "instructions": "Stand with feet shoulder-width. Lower hips until thighs are parallel to the floor. Keep chest up.",
        },
        {
            "name": "Push-Up",
            "sets": 3,
            "reps": 10,
            "rest_seconds": 30,
            "instructions": "Hands slightly wider than shoulders. Lower chest to the floor, then push back up.",
        },
        {
            "name": "Glute Bridge",
            "sets": 3,
            "reps": 15,
            "rest_seconds": 30,
            "instructions": "Lie on your back, knees bent. Drive hips up, squeeze glutes at the top.",
        },
    ],
    cool_down=[
        {
            "name": "Standing Quad Stretch",
            "duration_seconds": 30,
            "instructions": "Stand on one leg, hold the other ankle behind you for 30 seconds each side.",
        },
        {
            "name": "Child's Pose",
            "duration_seconds": 30,
            "instructions": "Kneel and sit back on your heels, stretch arms forward on the floor.",
        },
    ],
    safety_note=(
        "Stop immediately if you feel pain. Consult a healthcare professional "
        "before starting any new exercise program."
    ),
)


async def generate_workout(
    profile: Optional[UserProfile] = None,
    override_duration: Optional[int] = None,
    override_equipment: Optional[str] = None,
) -> WorkoutResponse:
    """Generate a personalised workout via IBM Granite."""
    if profile and override_duration:
        profile.workout_duration_minutes = override_duration
    if profile and override_equipment:
        profile.equipment = override_equipment

    system = prompts.workout_system_prompt(profile)
    user_msg = (
        f"Create a {profile.workout_duration_minutes if profile else 30}-minute "
        f"{'home ' if (not profile or profile.equipment == 'none') else ''}"
        f"workout for a {profile.experience_level if profile else 'beginner'} "
        f"whose goal is {profile.fitness_goal if profile else 'general fitness'}."
    )

    try:
        raw = await granite.granite_json(system, user_msg, max_tokens=1200)
        return parse_workout(raw)
    except Exception as exc:
        logger.warning("Workout generation failed, using fallback: %s", exc)
        return _FALLBACK_WORKOUT
