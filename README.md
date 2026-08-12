# Task Tracker (Module 1)

A learning-project REST API built with FastAPI, implementing task CRUD,
filtering by status/priority, and forward-only status transitions.
Persistence is in-memory (`backend/app/storage.py`) — see
[`docs/ADR-001.md`](docs/ADR-001.md) for the architecture decision. No auth, no database, no
Docker, no deployment in this module.

## Project structure

```
task-tracker/
├── backend/
│   ├── app/            # FastAPI application code
│   ├── data/           # tasks.json (created at runtime)
│   ├── tests/          # pytest suite
│   ├── requirements.txt
│   └── .env.example
├── frontend/            # HTML/CSS/JS UI (added later)
└── README.md
```

## Setup

1. Copy the environment file:
   - macOS/Linux: `cp backend/.env.example backend/.env`
   - Windows PowerShell: `copy backend\.env.example backend\.env`
2. Create a virtual environment and install dependencies (see below).

## Create venv, install dependencies, run server

**Windows PowerShell:**
```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Test the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-07-25T12:00:00.000000+00:00"
}
```

## Swagger UI

Once the server is running, open:

```
http://localhost:8000/docs
```