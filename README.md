# Project Builder Cost Estimator API

A comprehensive FastAPI service powered by configurable LLM providers (Cerebras or Gemini) that analyzes software project ideas — from cost estimation to pitch deck generation.

## Features

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Cost Estimation | `POST /api/v2/estimate-cost` | Deep + MVP cost breakdown with timeline |
| Idea Refinement | `POST /api/v2/refine-idea` | Clarifies vague ideas with Q&A |
| Full Analysis | `POST /api/v2/full-analysis` | All 7 analyses in parallel (premium) |
| MVP Roadmap | `POST /api/v2/roadmap` | Phased development plan |
| Revenue Estimator | `POST /api/v2/revenue` | Monetization model + MRR forecast |
| Competitor Analysis | `POST /api/v2/competitors` | Market gap & competitor breakdown |
| Risk Assessment | `POST /api/v2/risk` | Feasibility score with red flags |
| Team Generator | `POST /api/v2/team` | Roles, skills, rates & hiring strategy |
| Tech Stack Comparison | `POST /api/v2/tech-stack` | Open-source vs paid per category |
| Complexity Visualizer | `POST /api/v2/complexity` | Per-area complexity scores + reduction tips |
| Pitch Deck Generator | `POST /api/v2/pitch-deck` | Investor deck with speaker notes |
| Expert Chat | `POST /api/v2/chat` | Chat with PM, Architect, Investor, or General expert |
| Chat Summary | `POST /api/v2/chat/summary` | Summarize a chat session |
| Project Persistence | `CRUD /api/v2/projects` | Save, list, update, delete projects |

## Quick Start

### 1. Prerequisites

- Python 3.11+
- A [Gemini API Key](https://aistudio.google.com/apikey)

### 2. Setup

```bash
# Clone the repo
git clone https://github.com/ABL4Z3/project-builder.git
cd project-builder

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set CEREBRAS_API_KEY (recommended)
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

Open Swagger docs: **http://127.0.0.1:8000/docs**

### 4. Docker (Optional)

```bash
# Build and run
docker-compose up --build

# Or just Docker
docker build -t project-builder .
docker run -p 8000:8000 --env-file .env project-builder
```

## API Authentication

By default, auth is **disabled** (development mode). To enable:

1. Set `API_AUTH_TOKEN=your_secret_token` in `.env`
2. Send `X-API-Key: your_secret_token` header with every request

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `auto` | LLM provider: `auto`, `cerebras`, or `gemini` |
| `CEREBRAS_API_KEY` | *(recommended)* | Your Cerebras API key |
| `CEREBRAS_MODEL` | `llama3.1-8b` | Cerebras model to use |
| `GEMINI_API_KEY` | *(optional fallback)* | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model to use |
| `API_AUTH_TOKEN` | *(empty = disabled)* | API key for authentication |
| `PB_DATABASE_URL` | `sqlite+aiosqlite:///./project_builder.db` | Database connection URL |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins (JSON) |
| `RATE_LIMIT_PER_MINUTE` | `10` | Rate limit per IP per minute |
| `CACHE_TTL_SECONDS` | `3600` | Cache time-to-live in seconds |

## Architecture

```
project-builder/
├── app/
│   ├── main.py              # FastAPI app, CORS, rate limiting, lifespan
│   ├── core/
│   │   ├── config.py        # Pydantic Settings from .env
│   │   ├── auth.py          # API key authentication
│   │   ├── cache.py         # In-memory TTL cache
│   │   ├── database.py      # SQLAlchemy async engine + session
│   │   └── logging_config.py
│   ├── models/
│   │   └── project.py       # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── estimation.py    # Cost estimation schemas
│   │   ├── refinement.py    # Idea refinement schemas
│   │   ├── roadmap.py       # MVP roadmap schemas
│   │   ├── revenue.py       # Revenue estimation schemas
│   │   ├── competitor.py    # Competitor analysis schemas
│   │   ├── risk.py          # Risk assessment schemas
│   │   ├── team.py          # Team generator schemas
│   │   ├── tech_stack.py    # Tech stack comparison schemas
│   │   ├── complexity.py    # Complexity visualizer schemas
│   │   ├── pitch_deck.py    # Pitch deck generator schemas
│   │   ├── chat.py          # Expert chat schemas
│   │   ├── full_analysis.py # Full analysis schemas
│   │   └── project.py       # Project persistence schemas
│   ├── services/
│   │   ├── gemini_service.py       # Async Gemini client with retry + caching
│   │   ├── estimation_service.py
│   │   ├── refinement_service.py
│   │   ├── roadmap_service.py
│   │   ├── revenue_service.py
│   │   ├── competitor_service.py
│   │   ├── risk_service.py
│   │   ├── team_service.py
│   │   ├── tech_stack_service.py
│   │   ├── complexity_service.py
│   │   ├── pitch_deck_service.py
│   │   ├── chat_service.py
│   │   └── project_service.py
│   └── routers/
│       ├── estimation.py    # Cost estimation endpoint
│       ├── refinement.py    # Idea refinement endpoint
│       ├── analysis.py      # All analysis + complexity + pitch deck endpoints
│       ├── chat.py          # Expert chat + summary endpoints
│       └── projects.py      # Project CRUD + estimate storage
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Procfile                 # Railway deployment
└── README.md
```

## Key Improvements Over v1

- **Security**: API key auth via header (not URL), CORS middleware, rate limiting, no internal error exposure
- **Performance**: Async HTTP with httpx, parallel analysis with `asyncio.gather`, in-memory TTL cache
- **Reliability**: Retry with exponential backoff (tenacity), Pydantic schema validation on AI output
- **Database**: SQLAlchemy async with SQLite (swap to PostgreSQL for production)
- **Chat Persistence**: Chat sessions stored in database (not in-memory)
- **12 Endpoints**: From 1 endpoint in v1 to 14 endpoints in v2
- **Structured Output**: Every AI response validated against strict Pydantic schemas

## Deploy on Railway

1. Push this project to GitHub.
2. In Railway, create a new project → **Deploy from GitHub Repo**.
3. Select this repository.
4. Add environment variables:
  - `CEREBRAS_API_KEY=your_real_key`
  - `LLM_PROVIDER=cerebras`
   - `GEMINI_MODEL=gemini-2.5-flash`
5. Railway will run the `Procfile` command automatically.

## Sample Requests

### Cost Estimation
```json
POST /api/v2/estimate-cost
{
  "project_idea": "I need a B2B SaaS platform for restaurant inventory, purchasing and analytics with mobile access.",
  "currency": "INR"
}
```

### Chat with Expert
```json
POST /api/v2/chat
{
  "project_idea": "How should I price my SaaS product?",
  "session_id": "",
  "mode": "investor"
}
```

### Full Analysis (Premium)
```json
POST /api/v2/full-analysis
{
  "project_idea": "A food delivery app with real-time tracking and subscription meals.",
  "currency": "INR"
}
```

### Pitch Deck
```json
POST /api/v2/pitch-deck
{
  "project_idea": "AI-powered personal finance app for Gen Z.",
  "currency": "INR"
}
```

## License

MIT
