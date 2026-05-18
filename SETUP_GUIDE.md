# Project Builder API — Complete Setup Guide

This guide walks you through setting up the Project Builder Cost Estimator API from scratch on your local machine.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Step 1: Clone the Repository](#2-step-1-clone-the-repository)
3. [Step 2: Create Virtual Environment](#3-step-2-create-virtual-environment)
4. [Step 3: Install Dependencies](#4-step-3-install-dependencies)
5. [Step 4: Configure Environment Variables](#5-step-4-configure-environment-variables)
6. [Step 5: Run the Server](#6-step-5-run-the-server)
7. [Step 6: Test the API](#7-step-6-test-the-api)
8. [Docker Setup (Alternative)](#8-docker-setup-alternative)
9. [Production Deployment](#9-production-deployment)
10. [Switching to PostgreSQL](#10-switching-to-postgresql)
11. [Enabling Authentication](#11-enabling-authentication)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Prerequisites

Before you start, make sure you have:

- **Python 3.11 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **A Gemini API Key** — Get one free at [Google AI Studio](https://aistudio.google.com/apikey)
- **Git** — [Download Git](https://git-scm.com/downloads)
- *(Optional)* **Docker & Docker Compose** — for containerized setup

Verify Python:
```bash
python --version
# Should show Python 3.11.x or higher
```

---

## 2. Step 1: Clone the Repository

```bash
git clone https://github.com/ABL4Z3/project-builder.git
cd project-builder
```

---

## 3. Step 2: Create Virtual Environment

A virtual environment keeps project dependencies isolated from your system Python.

### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

---

## 4. Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI** — Web framework
- **Uvicorn** — ASGI server
- **httpx** — Async HTTP client for Gemini API
- **Pydantic** — Data validation & settings
- **SQLAlchemy + aiosqlite** — Async database ORM + SQLite driver
- **slowapi** — Rate limiting
- **tenacity** — Retry logic with exponential backoff
- **cachetools** — In-memory TTL cache
- **python-jose + passlib** — Auth token support

Verify installation:
```bash
pip list
```

---

## 5. Step 4: Configure Environment Variables

Copy the example env file and edit it:

```bash
cp .env.example .env
```

**Open `.env` in any text editor** and set your LLM provider/API key:

```env
# ── Required ──
LLM_PROVIDER=cerebras
CEREBRAS_API_KEY=your_cerebras_api_key_here
CEREBRAS_MODEL=llama3.1-8b

# ── Optional fallback ──
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

# ── Optional (defaults are fine for development) ──
API_AUTH_TOKEN=
PB_DATABASE_URL=sqlite+aiosqlite:///./project_builder.db
CORS_ORIGINS=["*"]
RATE_LIMIT_PER_MINUTE=10
CACHE_TTL_SECONDS=3600
```

### How to Configure Provider Keys:
1. Set `LLM_PROVIDER=cerebras` and add your `CEREBRAS_API_KEY`.
2. Optionally keep `GEMINI_API_KEY` set as fallback when using `LLM_PROVIDER=auto`.

---

## 6. Step 5: Run the Server

### Development (with auto-reload):
```bash
uvicorn app.main:app --reload
```

### Production:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Open Interactive Docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 7. Step 6: Test the API

### Health Check
```bash
curl http://127.0.0.1:8000/health
```
Expected: `{"status":"ok","version":"2.0.0"}`

### Cost Estimation
```bash
curl -X POST http://127.0.0.1:8000/api/v2/estimate-cost \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "I need a B2B SaaS platform for restaurant inventory management with mobile access",
    "currency": "USD"
  }'
```

### Chat with Expert
```bash
curl -X POST http://127.0.0.1:8000/api/v2/chat \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "How should I price my SaaS product?",
    "session_id": "",
    "mode": "investor"
  }'
```

### Full Analysis (all 7 analyses in parallel)
```bash
curl -X POST http://127.0.0.1:8000/api/v2/full-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "A food delivery app with real-time tracking and subscription meals",
    "currency": "USD"
  }'
```

### Pitch Deck
```bash
curl -X POST http://127.0.0.1:8000/api/v2/pitch-deck \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "AI-powered personal finance app for Gen Z",
    "currency": "USD"
  }'
```

### Complexity Analysis
```bash
curl -X POST http://127.0.0.1:8000/api/v2/complexity \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "A multi-vendor marketplace with real-time bidding and escrow payments",
    "currency": "USD"
  }'
```

### Save a Project
```bash
curl -X POST http://127.0.0.1:8000/api/v2/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_idea": "A food delivery app with real-time tracking",
    "project_name": "FoodDash",
    "currency": "USD"
  }'
```

### With Authentication (if enabled)
```bash
curl -X POST http://127.0.0.1:8000/api/v2/estimate-cost \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secret_token" \
  -d '{"project_idea": "...", "currency": "USD"}'
```

---

## 8. Docker Setup (Alternative)

If you prefer Docker:

### Using Docker Compose (recommended):
```bash
# Make sure .env file exists with your LLM API key(s)
docker-compose up --build
```

### Using Docker directly:
```bash
# Build
docker build -t project-builder .

# Run
docker run -p 8000:8000 --env-file .env project-builder
```

The API will be available at http://localhost:8000

---

## 9. Production Deployment

### Railway

1. Push this project to GitHub.
2. In [Railway](https://railway.app/), create a new project → **Deploy from GitHub Repo**.
3. Select this repository.
4. Add environment variables in Railway dashboard:
  - `LLM_PROVIDER=cerebras`
  - `CEREBRAS_API_KEY=your_real_key`
   - `GEMINI_MODEL=gemini-2.5-flash`
   - `API_AUTH_TOKEN=a_secure_random_token`
5. Railway auto-detects the `Procfile` and runs the server.

### Render

1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repo.
3. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in the Render dashboard.

### Fly.io

```bash
fly launch
fly secrets set LLM_PROVIDER=cerebras
fly secrets set CEREBRAS_API_KEY=your_key
fly deploy
```

---

## 10. Switching to PostgreSQL

For production, use PostgreSQL instead of SQLite.

### 1. Install asyncpg:
```bash
pip install asyncpg
```

Uncomment `asyncpg==0.30.0` in `requirements.txt`.

### 2. Update .env:
```env
PB_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/project_builder
```

### 3. Using Docker Compose with PostgreSQL:

Uncomment the `db` service in `docker-compose.yml`, then:

```bash
docker-compose up --build
```

---

## 11. Enabling Authentication

By default, the API runs without authentication. To secure it:

1. Generate a secure token:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. Add it to `.env`:
   ```env
   API_AUTH_TOKEN=your_generated_token_here
   ```

3. All endpoints now require the `X-API-Key` header:
   ```
   X-API-Key: your_generated_token_here
   ```

---

## 12. Troubleshooting

### "LLM API key is not set"
- Make sure `.env` file exists in the project root
- Verify `CEREBRAS_API_KEY` (or `GEMINI_API_KEY`) has your actual key (no quotes, no spaces)

### "ModuleNotFoundError"
- Make sure virtual environment is activated: `(.venv)` in prompt
- Run `pip install -r requirements.txt` again

### "Address already in use"
- Another process is using port 8000. Kill it:
  ```bash
  # Find the process
  lsof -i :8000  # macOS/Linux
  netstat -ano | findstr 8000  # Windows

  # Or use a different port:
  uvicorn app.main:app --port 8001
  ```

### "The AI returned data that could not be validated"
- LLM output can vary slightly in JSON formatting. Retry the request.
- The cache may have stale data — restart the server to clear the in-memory cache.

### Slow responses
- First requests are slower (LLM API call + cold start)
- Subsequent identical requests are cached (1-hour TTL by default)
- The `/full-analysis` endpoint runs 7 analyses in parallel for speed

### Database issues
- Delete `project_builder.db` and restart the server to recreate tables
- For PostgreSQL, ensure the database exists and credentials are correct

---

## API Endpoints Summary

| Method | Endpoint | Auth | Rate Limit | Description |
|--------|----------|------|------------|-------------|
| GET | `/health` | No | None | Health check |
| POST | `/api/v2/estimate-cost` | Optional | 10/min | Cost estimation |
| POST | `/api/v1/estimate-cost` | Optional | 10/min | v1 backward compatible |
| POST | `/api/v2/refine-idea` | Optional | None | Idea refinement |
| POST | `/api/v2/full-analysis` | Optional | None | All analyses (parallel) |
| POST | `/api/v2/roadmap` | Optional | None | MVP roadmap |
| POST | `/api/v2/revenue` | Optional | None | Revenue estimation |
| POST | `/api/v2/competitors` | Optional | None | Competitor analysis |
| POST | `/api/v2/risk` | Optional | None | Risk assessment |
| POST | `/api/v2/team` | Optional | None | Team generator |
| POST | `/api/v2/tech-stack` | Optional | None | Tech stack comparison |
| POST | `/api/v2/complexity` | Optional | None | Complexity visualizer |
| POST | `/api/v2/pitch-deck` | Optional | None | Pitch deck generator |
| POST | `/api/v2/chat` | Optional | None | Expert chat |
| POST | `/api/v2/chat/summary` | Optional | None | Chat session summary |
| POST | `/api/v2/projects` | Optional | None | Create project |
| GET | `/api/v2/projects` | Optional | None | List projects |
| GET | `/api/v2/projects/{id}` | Optional | None | Get project |
| PATCH | `/api/v2/projects/{id}` | Optional | None | Update project |
| DELETE | `/api/v2/projects/{id}` | Optional | None | Delete project |
| GET | `/api/v2/projects/{id}/estimates` | Optional | None | Get project estimates |
| POST | `/api/v2/projects/{id}/estimates` | Optional | None | Save estimate to project |
