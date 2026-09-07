# Fitness Buddy 💪

> **An AI-powered health and fitness assistant** providing personalised home workouts, motivational tips, nutritious meal suggestions, and habit-building guidance — powered by IBM Granite AI.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [IBM Granite Configuration](#ibm-granite-configuration)
6. [Environment Variables](#environment-variables)
7. [Running the Application](#running-the-application)
8. [API Endpoints](#api-endpoints)
9. [Architecture](#architecture)
10. [Troubleshooting](#troubleshooting)
11. [Disclaimer](#disclaimer)
12. [Author & Acknowledgments](#Author--&--Acknowledgments)

---

## Overview

Fitness Buddy is a full-stack MVP web application built for a hackathon. It uses:

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.11+, FastAPI, Pydantic, Uvicorn |
| AI | IBM Granite via IBM watsonx |
| Environment | Python virtual environment (`.venv`) |

**Features:**
- 🏋️ Personalised home workout generation
- 🥗 Healthy meal suggestions matched to dietary preferences
- 💬 Free-form AI chat coach
- ✅ Daily habit tracker with streak counter
- ✨ Daily AI-generated motivation quote
- 📊 Single-page dashboard

---

## Prerequisites

- **Python 3.11 or 3.12** — [python.org](https://www.python.org/downloads/)
- **IBM Cloud account** with watsonx.ai access
- **IBM Granite project** — `ibm/granite-4-h-small` model enabled
- A terminal (PowerShell, bash, or zsh)

---

## Project Structure

```
fitness-buddy/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, static file serving, router mounts
│   │   ├── api/
│   │   │   ├── chat.py          # POST /api/chat
│   │   │   ├── workout.py       # POST /api/workout
│   │   │   ├── nutrition.py     # POST /api/nutrition
│   │   │   ├── profile.py       # POST /api/profile
│   │   │   └── habits.py        # GET /api/habits, GET /api/motivation
│   │   ├── ai/
│   │   │   ├── granite.py       # IBM Granite HTTP client + IAM token exchange
│   │   │   ├── prompts.py       # System prompts per feature
│   │   │   └── schemas.py       # Pydantic validators for AI responses
│   │   ├── services/
│   │   │   ├── workout_service.py
│   │   │   ├── nutrition_service.py
│   │   │   └── habit_service.py
│   │   └── models/
│   │       └── schemas.py       # Shared Pydantic models
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html               # Landing page
│   ├── profile.html             # Profile setup
│   ├── dashboard.html           # Main dashboard
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   └── js/
│       ├── app.js               # Shared utilities + bootstrap
│       ├── api.js               # Fetch wrappers
│       ├── chat.js              # Chat panel
│       ├── workout.js           # Workout renderer
│       ├── nutrition.js         # Nutrition renderer
│       ├── habits.js            # Habit tracker (localStorage)
│       └── profile.js           # Profile read/write (localStorage)
├── run.sh                       # Convenience start script (Linux/macOS)
├── gitignore.txt                # Rename to .gitignore
└── README.md
```

---

## Setup & Installation

### 1. Clone / navigate to the project

```bash
cd fitness-buddy
```

### 2. Create the Python virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

You will see `(.venv)` in your prompt when the environment is active.

### 4. Install dependencies

```bash
pip install -r backend/requirements.txt
```

> ⚠️ Always activate the virtual environment first. Never install project packages globally.

---

## IBM Granite Configuration

### Step 1 – Create your `.env` file

```bash
cp backend/.env.example backend/.env
```

### Step 2 – Fill in your credentials

Open `backend/.env` and set the values:

```env
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
WATSONX_PROJECT_ID=<your watsonx project ID>
GRANITE_MODEL_ID=ibm/granite-4-h-small
```

### Where to find your credentials

| Variable | Where to find it |
|---|---|
| `WATSONX_API_KEY` | IBM Cloud → Manage → Access (IAM) → API keys |
| `WATSONX_PROJECT_ID` | watsonx.ai → Your project → Manage → General → Project ID |
| `WATSONX_URL` | Fixed endpoint (already set in `.env.example`) |
| `GRANITE_MODEL_ID` | Fixed model ID (already set in `.env.example`) |

> 🔒 **Never commit `.env` to Git.** Add `.gitignore` (rename `gitignore.txt`) to protect secrets.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WATSONX_API_KEY` | ✅ Yes | IBM Cloud API key for IAM authentication |
| `WATSONX_URL` | ✅ Yes | watsonx chat endpoint URL |
| `WATSONX_PROJECT_ID` | ✅ Yes | watsonx project ID |
| `GRANITE_MODEL_ID` | ✅ Yes | Granite model identifier |
| `APP_HOST` | Optional | Server host (default: `0.0.0.0`) |
| `APP_PORT` | Optional | Server port (default: `8000`) |

---

## Running the Application

### Make sure the virtual environment is active

**Windows:**
```powershell
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### Start the server

From the `fitness-buddy/` root directory:

```bash
uvicorn backend.app.main:app --reload
```

Or using the helper script (Linux/macOS):

```bash
bash run.sh
```

### Open in browser

```
http://localhost:8000
```

**Pages:**
- `http://localhost:8000/` — Landing page
- `http://localhost:8000/profile` — Profile setup
- `http://localhost:8000/dashboard` — Main dashboard
- `http://localhost:8000/docs` — Auto-generated API docs (Swagger UI)

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serve landing page |
| `GET` | `/profile` | Serve profile page |
| `GET` | `/dashboard` | Serve dashboard page |
| `POST` | `/api/profile` | Validate and return user profile |
| `POST` | `/api/chat` | Free-form AI chat with IBM Granite |
| `POST` | `/api/workout` | Generate personalised workout plan |
| `POST` | `/api/nutrition` | Get healthy meal suggestions |
| `GET` | `/api/habits` | Get default habit catalogue |
| `GET` | `/api/motivation` | Get daily motivational quote + tip |
| `GET` | `/docs` | Swagger UI (auto-generated) |

---

## Architecture

```
Browser (HTML/CSS/Vanilla JS)
        ↓  HTTP fetch
FastAPI (backend/app/main.py)
        ↓
API Routes (backend/app/api/)
        ↓
Application Services (backend/app/services/)
        ↓
IBM Granite AI Client (backend/app/ai/granite.py)
        ↓  HTTPS + IAM token
IBM Cloud / watsonx.ai
        ↓
Structured JSON response
        ↓
Pydantic validation (backend/app/ai/schemas.py)
        ↓
FastAPI JSON response
        ↓
Vanilla JavaScript renders UI
```

**Key design decisions:**
- IBM credentials live only in `backend/.env` — never sent to the browser
- IAM token exchange is cached in-process and refreshed on 401
- All AI responses are validated with Pydantic before returning to the client
- Graceful fallback content is returned when Granite is unavailable
- Habit state is stored in `localStorage` — no database needed for MVP

---

## Troubleshooting

### `WATSONX_API_KEY is not set`
→ Copy `backend/.env.example` to `backend/.env` and fill in your IBM credentials.

### `HTTP 401` from Granite
→ Your API key may have expired or is incorrect. Regenerate it in IBM Cloud IAM.

### `HTTP 403` from Granite
→ Your project ID may be wrong, or the Granite model is not enabled for your project.

### Module not found errors
→ Ensure the virtual environment is activated and you ran `pip install -r backend/requirements.txt`.

### `uvicorn: command not found`
→ Activate the virtual environment first (`.venv\Scripts\activate` on Windows).

### Static files not loading (404)
→ Run uvicorn from the `fitness-buddy/` root directory, not from inside `backend/`.

### AI responses are slow
→ Normal — IBM watsonx API calls can take 5-15 seconds. The UI shows a loading spinner.

### Port 8000 already in use
→ Use `uvicorn backend.app.main:app --reload --port 8001` and visit `http://localhost:8001`.

---

## Disclaimer

**Fitness Buddy provides general wellness information only.**

It is **not** a substitute for professional medical advice, diagnosis, or treatment. Do not use Fitness Buddy to diagnose or treat any medical condition. For injuries, medical conditions, pregnancy, or any health concerns, consult a qualified healthcare professional before starting any new exercise or nutrition program.

---

## 👤 Author & Acknowledgments

- **Intern / Author:** Arnab Chowdhury.
- **Internship Program:**  IBM SKILLSBUILD FOR UNIVERSITY ENGAGEMENTS ON AI & IBM CLOUD
- **Organized By:** IBM Skills Build
- **In Collaboration With:** Edunet Foundation & AICTE (All India Council for Technical Education)
