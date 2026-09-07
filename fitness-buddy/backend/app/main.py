"""
Fitness Buddy – FastAPI application entry point.
Serves the frontend static files and mounts all API routers.
"""
import sys
from pathlib import Path

# Ensure 'backend/' is on sys.path so 'app.*' imports resolve when uvicorn
# is launched as `uvicorn backend.app.main:app` from the project root.
_BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load .env from backend/ directory regardless of working directory
load_dotenv(_BACKEND_DIR / ".env")

from app.api import chat, workout, nutrition, profile, habits  # noqa: E402

app = FastAPI(
    title="Fitness Buddy API",
    description="AI-powered health and fitness assistant powered by IBM Granite",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")


@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/profile", include_in_schema=False)
async def serve_profile():
    return FileResponse(FRONTEND_DIR / "profile.html")


@app.get("/dashboard", include_in_schema=False)
async def serve_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


# ---------------------------------------------------------------------------
# API routers
# ---------------------------------------------------------------------------
app.include_router(profile.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(workout.router, prefix="/api")
app.include_router(nutrition.router, prefix="/api")
app.include_router(habits.router, prefix="/api")
