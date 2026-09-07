#!/usr/bin/env bash
# run.sh – Start the Fitness Buddy application
# Usage: bash run.sh

set -e

echo "======================================"
echo "  Fitness Buddy – Starting Server"
echo "======================================"

# Activate virtual environment (Linux/macOS)
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
  echo "✅ Virtual environment activated"
elif [ -f ".venv/Scripts/activate" ]; then
  # Windows Git Bash
  source .venv/Scripts/activate
  echo "✅ Virtual environment activated (Windows)"
else
  echo "⚠️  No .venv found. Create it with: python -m venv .venv"
  echo "    Then install deps: pip install -r backend/requirements.txt"
  exit 1
fi

# Check .env exists
if [ ! -f "backend/.env" ]; then
  echo "⚠️  backend/.env not found. Copy backend/.env.example to backend/.env and fill in your credentials."
  exit 1
fi

echo "🚀 Starting FastAPI server at http://localhost:8000"
echo "   Press Ctrl+C to stop."
echo ""

cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
