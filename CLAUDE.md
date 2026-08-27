#Task Tracker

## Stack
- Python 3.11
- FastAPI + Pydantic v2 + Uvicorn
- pytest + httpx for tests
- Vanilla Javascript frontend in frontend/index.html

## Run
- Server: uvicorn app.main:app --reload --port 8000
- Tests: pytest -v
- Frontend: open frontend/index.html with live Server, or use the local serving approach from Module 3

## Architecture
- backend/app/main.py: FastAPI app, routes, CORS middleware, and route handlers
- backend/app/models.py: Pydantic schemas and validation types
- backend/app/storage.py: in-memory task store
- tests/: pytest tests
- frontend/index.html: Kanban board UI 

## Business Rules that must not be violated
- Valid Transitions: ToDo -> InProgress, InProgress -> Done, Done -> InProgress
- Invalid Transitions: ToDo -> Done, Done -> ToDo, InProgress -> ToDo
- No-op behavior Transitions: same status -> same status
- Invalid Transitions return 422
- Title are required, trimmed and non-empty
- Frontend must keep loading, empty, error, and populated states
- Frontend status must remain ToDo, InProgress, Done

## Do Not
- Do not add authentication
- Do not introduce database without asking
- Do not change public response shapes without explicit approval
- Do not remove test to make CI pass
- Do not run destructive shell commands without explicit confirmation
- Do not use always allow for broad shell permissions

@README.md
