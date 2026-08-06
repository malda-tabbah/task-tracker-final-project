# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Task Tracker (Module 1) — a learning project. FastAPI backend with local JSON
persistence (`backend/data/tasks.json`, no database), plain HTML/CSS/JS
frontend with no build step. No auth, no Docker, no CI.

## Backend (`backend/`)

FastAPI + Pydantic v2, Python. Entry point: `backend/app/main.py`.

Setup:
```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy backend\.env.example backend\.env   # if not already present
```

Run: `uvicorn app.main:app --reload --port 8000` (from `backend/`)

Test: `pytest` (from `backend/`; config in `pytest.ini`, suite is
`backend/tests/test_tasks.py`). `backend/tests/verify_a.py` is a standalone
manual script (uses `print`, no assertions) — not part of the pytest suite,
don't treat failures/output from it as test results.

No lint/formatter is configured for the backend.

`backend/app/routes.py` and `backend/app/service.py` are empty/unused —
routes and logic live in `main.py`, `storage.py`, and `business_rules.py`.
Don't assume code belongs in the empty files just because their names suggest it.

Status transitions are restricted (`backend/app/business_rules.py`):
only `todo→in_progress`, `in_progress→done`, and `in_progress→todo` (reopening)
are valid. Direct `todo→done` or `done→todo` is rejected with a 422.

## Frontend (`frontend/`)

Single file, `frontend/index.html` — inline `<style>`/`<script>`, no
framework, no package manager, no build step. Open directly or serve with a
static server.

API base URL is hardcoded: `const API_URL = 'http://localhost:8000'`. Backend
CORS (`allow_origins` in `backend/app/main.py`) only permits
`http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, and
`file://` (`"null"` origin). If serving the frontend from a different
port/origin, update `allow_origins` in `main.py` to match.
