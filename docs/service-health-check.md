# Service Health Check

## Purpose

This procedure records the local backend health, frontend visibility, and automated test baseline for the end-course Task Tracker project.

Review date: 2026-08-23.

## Backend Baseline

Command used to start the API, from `backend`:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Observed startup result:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

Health check command, from the repository root:

```powershell
curl.exe -s http://localhost:8000/health
```

Result:

```json
{"status":"ok","timestamp":"2026-08-23T10:57:07.983864+00:00"}
```

## Frontend Baseline

Command used to open the frontend, from `frontend`:

```powershell
py -m http.server 5500
```

Frontend URL opened in the browser:

```text
http://localhost:5500/
```

Result: the Task Board page showed the ToDo, InProgress, and Done Kanban columns, and a temporary in-memory task was created and opened in the Edit Task modal, confirming the Kanban board/create-edit flow was still visible.

No video evidence is required.

## Test Baseline

Command used to run the full pytest suite, from `backend`:

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

Result:

```text
48 passed in 1.01s
```

No tests failed, so there were no failing test names to classify as pre-existing or introduced by final work.

## CI Workflow Result

The end-course documentation changes were pushed to `origin/end-course-project`, which triggered the GitHub Actions `CI` workflow.

Workflow run:

```text
https://github.com/malda-tabbah/task-tracker/actions/runs/32635785571
```

Test job:

```text
https://github.com/malda-tabbah/task-tracker/actions/runs/32635785571/job/97185221189
```

Result:

```text
CI run 10 completed successfully for commit 7042ec3c5fbe37be738f31bea262606766231da8.
The workflow test job collected 48 tests and completed with 48 passed in 0.27s.
```

## Public Repository Workflow Evidence

The public end-course repository also ran the GitHub Actions `CI` workflow on `main`.

Public repository workflow run:

```text
https://github.com/malda-tabbah/end-course-project/actions/runs/32639820508
```

Public repository test job:

```text
https://github.com/malda-tabbah/end-course-project/actions/runs/32639820508/job/97195071938
```

Result:

```text
CI run 2 completed successfully for commit 94d00568c21c2758745c8b05a8ac26e11924d8d3.
The public Actions summary showed the test job succeeded in 11s and listed the Run tests step.
Detailed public job logs were not visible without signing in to GitHub.
```
