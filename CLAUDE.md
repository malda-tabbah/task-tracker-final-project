# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Tech stack

- Python [VERIFY: 3.11 — not pinned in repo; local venv reports 3.13.14]
- FastAPI `0.115.0`, Pydantic `2.9.2`, Uvicorn `0.30.6` (`backend/requirements.txt`)
- pytest `9.1.1`, httpx `0.28.1` (TestClient)
- python-dotenv `1.0.1`
- Frontend: vanilla HTML/CSS/JavaScript in `frontend/index.html` (no build step)

## 2. Run command

From `backend/` (venv active):

```powershell
uvicorn app.main:app --reload --port 8000
```

## 3. Test command

From `backend/` (venv active; `pytest.ini` sets `pythonpath = .`):

```powershell
pytest -v
```

Suite: `backend/tests/test_tasks.py` (+ `conftest.py`).
`backend/tests/verify_a.py` is a manual script (prints, no assertions) — not part of the pytest suite.

## 4. Architecture summary

- **Backend** (`backend/app/`):
  - `main.py` — FastAPI app, CORS, `/health` and task CRUD routes
  - `models.py` — `TaskStatus`, `TaskPriority`, `TaskCreate`, `TaskUpdate`, `TaskResponse`
  - `storage.py` — in-memory task store (`_tasks` dict); `_reset()` for tests
  - `business_rules.py` — status transition validation
  - `schemas.py` — `HealthResponse`
  - `routes.py`, `service.py` — empty/unused; do not assume logic belongs there
- **Frontend** (`frontend/index.html`) — single-file Task Board UI
- **Tests** (`backend/tests/`) — pytest + `TestClient`; real storage with autouse reset
- **Task rules** live in `backend/app/business_rules.py` (enforced on PATCH when `status` is set)

Persistence note: README mentions `backend/data/tasks.json`, but current `storage.py` keeps tasks in memory only. [VERIFY if JSON persistence is required for Module 4.]

## 5. Business rules

**Status values** (`models.py`): `ToDo` | `InProgress` | `Done`
**Priority values**: `Low` | `Medium` | `High`

**Allowed transitions** (`business_rules.py`):

| From | To |
|---|---|
| `ToDo` | `InProgress` |
| `InProgress` | `Done` |
| `Done` | `InProgress` |

- Same status → same status: allowed (no-op; validation returns early)
- Any other change (e.g. `ToDo` → `Done`): `422` with detail listing allowed transitions
- Title: required, non-blank after strip, max 200 chars; unknown fields forbidden (`extra="forbid"`)

## 6. UI states and CORS

**Board states** (`frontend/index.html`, `boardState`): `loading` | `ready` | `empty` | `error`

- Loading: skeleton columns
- Ready / empty: three columns (`ToDo`, `InProgress`, `Done`); empty columns show “Drop tasks here”
- Error: error card when fetch fails
- Drag-and-drop updates status via `PATCH /tasks/{id}`; client mirrors the same allowed transitions; invalid drops show “Invalid status transition.”
- Create/edit form with title/form error areas; `API_URL = 'http://localhost:8000'`

**CORS** (`main.py` `CORSMiddleware`):

- Origins: `http://localhost:5500`, `http://127.0.0.1:5500`, `http://localhost:5173`, `"null"` (file://)
- Methods/headers: `*`; `allow_credentials=False`
- Serving the UI from another origin requires updating `allow_origins`

## 7. Do-not rules

- Do not add authentication
- Do not add a database
- Do not add deployment / Docker / CI steps
- Do not make major UI redesigns without asking
- Do not invent features, routes, or transition rules not present in the code
