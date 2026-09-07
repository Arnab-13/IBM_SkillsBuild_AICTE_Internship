"""
Profile API – store/retrieve user profile (session cookie / localStorage backed).
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.schemas import UserProfile

router = APIRouter(tags=["profile"])


@router.post("/profile")
async def save_profile(profile: UserProfile):
    """Accept and validate a user profile. Returns the cleaned profile back."""
    return profile
