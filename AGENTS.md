# [AGENTS.md](http://AGENTS.md)

## Project Summary

Task Tracker is a learning-project task board with a Python FastAPI backend and a single vanilla HTML/CSS/JavaScript frontend.

The backend keeps one shared in-memory task list in `backend/app/storage.py` using a module-level `_tasks` dictionary. Data is lost when the API process restarts. No database persistence is visible in the current implementation.

The active API route handlers are in `backend/app/main.py`. `backend/app/routes.py` and `backend/app/service.py` are currently empty.

The frontend is `frontend/index.html`. It renders a three-column task board and calls the API at `http://localhost:8000`.

## Tech Stack

Confirmed from repository files:

- Python 3.11 is used by `Dockerfile` and `.github/workflows/ci.yml`; earlier Python versions are not confirmed.
- Backend: FastAPI, Uvicorn, Pydantic v2, python-dotenv.
- Tests: pytest and httpx/FastAPI TestClient.
- Frontend: vanilla HTML, CSS, and JavaScript in `frontend/index.html`.
- Packaging: root-level `Dockerfile` for local backend containerized runs only.
- `pyproject.toml`, `package.json`, and `backend/pyproject.toml` are not confirmed; they were not present during setup inspection.



## Supported Commands

Run commands from the repository root unless noted.

Backend setup on Windows PowerShell:

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the backend API locally:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Run the frontend locally:

```powershell
cd frontend
py -m http.server 5500
```

Run tests:

```powershell
cd backend
pytest -v
```

Run tests on Windows without activating the venv:

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest -v
```

Windows helper scripts:

```powershell
.\scripts\start.ps1
.\scripts\stop.ps1
```

Docker backend-only local run:

```powershell
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

Not confirmed: lint command, coverage command, formatter command, Docker Compose command, cloud deploy command.

## Business Rules Visible In Code

Task statuses are exactly:

- `ToDo`
- `InProgress`
- `Done`

Task priorities are exactly:

- `Low`
- `Medium`
- `High`

Status transitions:

- Allowed: `ToDo -> InProgress`
- Allowed: `InProgress -> Done`
- Allowed: `Done -> InProgress`
- Same-status updates are allowed as no-ops.
- Other status transitions raise HTTP 422.

Task creation and update validation:

- `title` is required on create.
- `title` is trimmed.
- Blank or whitespace-only titles are rejected.
- Titles longer than 200 characters are rejected.
- Unknown request fields are rejected by Pydantic `extra="forbid"`.
- `due_date` is required on create.
- Invalid due date formats are rejected.
- `due_date_change_date` is not client-settable on create because extra fields are forbidden.
- `overdue` is not client-settable on create because extra fields are forbidden.

Storage and derived fields:

- Task IDs are generated with `uuid4()`.
- `created_at` and `updated_at` use current UTC datetime.
- `due_date_change_date` starts as `None`.
- `due_date_change_date` changes only when a supplied `due_date` differs from the existing due date.
- `updated_at` changes on update.
- `overdue` is recomputed when tasks are returned.
- A task is overdue only when server date is later than `due_date` and status is `ToDo` or `InProgress`.
- `Done` tasks are never overdue.
- Missing `due_date` is treated as not overdue by `is_overdue`, though new task creation requires `due_date`.

Filtering and search:

- `GET /tasks` supports optional filters for `status`, `priority`, `assignee`, `due_date`, `overdue`, and `title`.
- Filters are applied together as logical AND.
- `assignee`, `status`, `priority`, and `due_date` filters are exact matches.
- `title` search is partial and case-insensitive.
- `overdue` filtering uses the computed overdue value.

API routes visible in `backend/app/main.py`:

- `GET /health`
- `GET /version`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`



## Frontend Behavior Visible In Code

The frontend:

- Uses a hardcoded API base URL: `http://localhost:8000`.
- Shows task columns for `ToDo`, `InProgress`, and `Done`.
- Supports loading, error, empty/no-match, and populated board states.
- Supports creating and editing tasks through a modal form.
- Requires title and due date in client-side form checks before submit.
- Supports deleting tasks after a browser confirmation prompt.
- Supports drag-and-drop status changes, with client-side transition checks matching the backend transition rules.
- Shows assignee, due date, due date change date, priority, and an overdue badge when present.
- Sends filters for title, assignee, due date, overdue, status, and priority.



## Module 5 Guardrails

Use docs-first workflow:

- Read `README.md` before changing behavior.
- Read relevant files under `docs/` before changing requirements, architecture notes, or reports.
- Read the implementation files before making claims about behavior.
- When docs and code conflict, call out the conflict and cite both; do not silently reconcile them.

Default to read-only:

- Inspect, summarize, and propose before editing unless the user explicitly asks for changes.
- Do not modify files outside the requested scope.
- Do not change `backend/app/` unless the user explicitly approves application-code changes.
- For AGENTS.md work, only edit `AGENTS.md` after approval.

One task per thread:

- Keep each Codex task focused on one user-requested outcome.
- Do not bundle unrelated refactors, formatting, documentation rewrites, or dependency changes into the same task.

No app changes without approval:

- Do not change backend route behavior, storage behavior, validation rules, public response shapes, frontend behavior, or tests unless explicitly requested.
- Preserve public route paths and field names unless the user explicitly approves a breaking change.
- Do not add authentication, a database, cloud deployment, or new infrastructure without explicit approval.



## Security And Governance

- Do not paste, print, commit, or expose secrets from `.env`, shell history, credentials, tokens, or local machine configuration.
- Do not run destructive commands such as `git reset --hard`, recursive deletion, broad process killing, or cleanup scripts without explicit confirmation.
- Do not run servers, long-running processes, Docker builds, installs, or tests unless they are needed for the requested task or the user approves them.
- Cite the exact files inspected when summarizing, reviewing, or making claims.
- Do not invent findings, test results, requirements, or architecture.
- If evidence is missing, say `not confirmed`.
- Treat generated cache files, virtual environments, `.pytest_cache`, and `__pycache__` as non-source artifacts unless the user specifically asks about them.
- Do not remove or weaken tests to make a task pass.
- Prefer small, targeted changes that match the existing repo style.

