# Task Tracker (Mid-Course Extension)

A learning-project task board: a FastAPI REST API plus a simple HTML/CSS/JavaScript UI. It keeps **one shared in-memory task list**. Data is lost when the API process restarts.

This is not production software. There is no authentication, database, Docker, or cloud deployment.

Architecture notes: `[docs/midcourse/mini-adr.md](docs/midcourse/mini-adr.md)`. User stories (US-08 to US-11): `[docs/midcourse/user-stories.md](docs/midcourse/user-stories.md)`.

## Project Report

The report is a PDF that summarises the mid-course work: what was done, the prompts used, and some frontend test screenshots. It consolidates the Markdown files in `[docs/midcourse/](docs/midcourse/)`.

PDF: `[docs/midcourse/Malda_Tabbah_SU25-26_MidCourse_Project.pdf](docs/midcourse/Malda_Tabbah_SU25-26_MidCourse_Project.pdf)`

## Features

- Create, view, update, and delete tasks
- Required due date on create; invalid dates are rejected
- Due date change date is set by the server only when the due date is changed after creation
- Overdue is derived: due date is in the past and status is `ToDo` or `InProgress`; `Done` is never overdue
- Filter and search by status, priority, due date, overdue flag, assignee, and title
- Status workflow: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`

## Project structure

```
task-tracker - mid/
├── backend/
│   ├── app/                 # FastAPI app, models, business rules, in-memory store
│   ├── tests/               # pytest suite
│   ├── requirements.txt
│   ├── pytest.ini
│   └── .env.example
├── frontend/
│   └── index.html           # Task board UI (expects API at http://localhost:8000)
├── docs/
│   └── midcourse/           # User stories, mini-ADR, verification, prompt log, report PDF
├── scripts/                 # Windows start/stop helpers
└── README.md
```

## Prerequisites

- Python 3.10 or later
- On Windows PowerShell, use `curl.exe` (plain `curl` is an alias for `Invoke-WebRequest`)

## Setup

1. Copy the environment file:
  - macOS/Linux: `cp backend/.env.example backend/.env`
  - Windows PowerShell: `copy backend\.env.example backend\.env`
2. Create a virtual environment and install dependencies (see below).

## Run the API

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

The API listens at `http://localhost:8000`. Swagger UI: `http://localhost:8000/docs`.

### Health check

```bash
curl.exe http://localhost:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "2026-08-16T12:00:00.000000+00:00"
}
```

## Run the UI

In a second terminal, from `frontend/`:

```powershell
py -m http.server 5500
```

Then open `http://localhost:5500`. The page calls `http://localhost:8000`.

On Windows you can start both servers and open the board with:

```powershell
.\scripts\start.ps1
```

Stop them with `.\scripts\stop.ps1` (or `scripts\start.bat` / `scripts\stop.bat`).

## Run tests

From `backend/`, with the venv active:

```powershell
python -m pytest
```

Windows without activating the venv:

```powershell
.\venv\Scripts\python.exe -m pytest
```

## API overview


| Method | Path               | Notes                                                                                   |
| ------ | ------------------ | --------------------------------------------------------------------------------------- |
| GET    | `/health`          | Liveness                                                                                |
| GET    | `/version`         | API version (`0.1.1`)                                                                   |
| GET    | `/tasks`           | Optional query params: `status`, `priority`, `assignee`, `due_date`, `overdue`, `title` |
| GET    | `/tasks/{task_id}` | 404 if missing                                                                          |
| POST   | `/tasks`           | `title` and `due_date` required                                                         |
| PATCH  | `/tasks/{task_id}` | Partial update; status changes follow the workflow above                                |
| DELETE | `/tasks/{task_id}` | 204 on success                                                                          |


## Docs


| File                                                                                                                     | Contents                       |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| `[docs/midcourse/user-stories.md](docs/midcourse/user-stories.md)`                                                       | Approved extension stories     |
| `[docs/midcourse/mini-adr.md](docs/midcourse/mini-adr.md)`                                                               | Architecture addendum          |
| `[docs/midcourse/verification.md](docs/midcourse/verification.md)`                                                       | Pytest results                 |
| `[docs/midcourse/backend_curl_tests_log.md](docs/midcourse/backend_curl_tests_log.md)`                                   | Manual curl checks             |
| `[docs/midcourse/break_test.md](docs/midcourse/break_test.md)`                                                           | Due-date validation break test |
| `[docs/midcourse/prompt-log.md](docs/midcourse/prompt-log.md)`                                                           | Major prompts used             |
| `[docs/midcourse/reflection.md](docs/midcourse/reflection.md)`                                                           | Reflection on AI use           |
| `[docs/midcourse/Malda_Tabbah_SU25-26_MidCourse_Project.pdf](docs/midcourse/Malda_Tabbah_SU25-26_MidCourse_Project.pdf)` | Course report PDF              |


