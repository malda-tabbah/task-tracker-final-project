# Part A - Baseline Preparation and Check

## A1. Creating and Verifying the End Project Baseline

Review date: 2026-08-23.

Baseline preparation evidence is documented in [prepare_end_baseline.md](prepare_end_baseline.md).

Summary:

- End-course work was performed from `C:\_Malda\Projects\task-tracker - end`.
- The active development branch was `end-course-project`.
- `origin` remained the private development repository.
- `end-public` was configured as the public end-course repository.
- The end-course branch was published to `end-public/main` at commit `f3367a9`.

Result: the mid-course project was preserved, and the end-course project was prepared in a separate folder, branch, and public release repository.

## A2. Verifying Successful Baseline Testing

Verification date: 2026-08-23.

The baseline service health and test procedure is documented in [service-health-check.md](service-health-check.md).

Baseline results recorded:

- Backend API startup and `GET /health` were verified successfully.
- Frontend access was verified by opening `http://localhost:5500/` and confirming that the Kanban board and create/edit flow were visible.
- The full backend pytest suite was run with `.\venv\Scripts\python.exe -m pytest -v`; result: `48 passed in 1.01s`.

# Part B - Release Readiness Evidence

## B1. CI Workflow

### B1.1 Workflow Verification

The `CI` workflow is triggered on every `push` and every `pull_request`. Once triggered, it runs on `ubuntu-latest`, sets up Python 3.11, installs the backend dependencies from `backend/requirements.txt`, and runs the backend test suite with `pytest -v` from the `backend` directory.

- Workflow: `[CI](https://github.com/malda-tabbah/task-tracker/actions/runs/32635785571)`, defined in `.github/workflows/ci.yml`.
- Trigger: push to `origin/end-course-project`.
- Pushed commit: `7042ec3c5fbe37be738f31bea262606766231da8` (`Record CI workflow evidence`).
- Workflow run: `CI` run 10, created at `2026-08-23T11:10:17Z` and completed successfully at `2026-08-23T11:10:32Z`.
- Test job: `[test](https://github.com/malda-tabbah/task-tracker/actions/runs/32635785571/job/97185221189)`, completed successfully.
- CI pytest result: `48 passed in 0.27s`.
- Public repository workflow evidence is also recorded in [service-health-check.md](service-health-check.md), including public `CI` run 2 on `main`, which completed successfully for commit `94d00568c21c2758745c8b05a8ac26e11924d8d3`.

### B1.2 Workflow Safety Review


| Check                                                | Pass/Concern | Evidence                                                                                  | Minimal fix                                                                                              |
| ---------------------------------------------------- | ------------ | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Missing push or pull_request trigger                 | Pass         | `.github/workflows/ci.yml` defines both `push` and `pull_request`.                        | None.                                                                                                    |
| Python version not pinned to 3.11                    | Pass         | The workflow uses `actions/setup-python@v5` with `python-version: "3.11"`.                | None.                                                                                                    |
| Dependencies installed but pytest never runs         | Pass         | The workflow installs dependencies, then runs `pytest -v`.                                | None.                                                                                                    |
| `continue-on-error` present                          | Pass         | No `continue-on-error` setting is present in the workflow.                                | None.                                                                                                    |
|                                                      |              | true present                                                                              | Pass                                                                                                     |
| `--exit-zero` present                                | Pass         | No `--exit-zero` flag is present.                                                         | None.                                                                                                    |
| Pytest output piped in a way that can hide exit code | Pass         | The workflow runs `pytest -v` directly with no pipe.                                      | None.                                                                                                    |
| Deployment steps that do not belong in this module   | Pass         | The workflow only checks out code, sets up Python, installs dependencies, and runs tests. | None.                                                                                                    |
| Workflow file located in the wrong folder            | Pass         | The workflow file is located at `.github/workflows/ci.yml`.                               | None. Use `.github/workflows/ci.yml` in evidence references, not the mistyped `.github/workflows/ci.ym`. |


### B1.3 Intentional Red-Run Evidence

Purpose: confirm that the `CI` workflow fails when pytest detects a failing test, then returns to green after the intentional break is reverted.


| Step                         | Evidence                                                                                                                                                                                                                                                                                                                                                           | Result                                                                                                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local break test             | Temporary file: `backend/tests/test_intentional_red_run.py`. Command: `.\venv\Scripts\python.exe -m pytest -v tests/test_intentional_red_run.py`.                                                                                                                                                                                                                  | Failed as intended: `tests/test_intentional_red_run.py::test_intentional_ci_red_run_fails`; result: `1 failed in 3.61s`.                                   |
| Red CI run                   | Commit: `f06dc3032e9101643e7da6ea8f21499a35004da3` (`Intentional CI red run`). Workflow: `[CI` run 12]([https://github.com/malda-tabbah/task-tracker/actions/runs/32646269736](https://github.com/malda-tabbah/task-tracker/actions/runs/32646269736)). Test job: `[test](https://github.com/malda-tabbah/task-tracker/actions/runs/32646269736/job/97210896045)`. | Failed as expected. CI log summary: `FAILED tests/test_intentional_red_run.py::test_intentional_ci_red_run_fails`; result: `1 failed, 48 passed in 0.20s`. |
| Revert and local green check | Revert commit: `3a081f34a857f0b5a0579ad6adfdc0a979f28fab` (`Revert "Intentional CI red run"`). The temporary failing test file was removed. Command: `.\venv\Scripts\python.exe -m pytest -v`.                                                                                                                                                                     | Local full suite passed after revert: `48 passed in 0.79s`.                                                                                                |
| Green CI run                 | Workflow: `[CI` run 13]([https://github.com/malda-tabbah/task-tracker/actions/runs/32646325653](https://github.com/malda-tabbah/task-tracker/actions/runs/32646325653)). Test job: `[test](https://github.com/malda-tabbah/task-tracker/actions/runs/32646325653/job/97211032548)`.                                                                                | Completed successfully. CI log summary: `48 passed in 0.27s`.                                                                                              |


## B2. Docker Image Verification Evidence

The local Docker image creation and run procedure is documented in [docker-image-creation.md](docker-image-creation.md). This section records the verification evidence for the Docker artifacts and the local image created for the end-course project.

### B2.1 Docker Artifact Safety Review


| Check                                                           | Evidence                                                                                                                                         | Result |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| Dockerfile uses a pinned slim base image                        | `Dockerfile` contains `FROM python:3.11-slim AS builder` and `FROM python:3.11-slim AS runtime`.                                                 | Pass   |
| Dockerfile does not use `python:latest`                         | `Select-String -Path Dockerfile -Pattern 'python:latest'` returned no unsafe base-image match.                                                   | Pass   |
| Dockerfile defines a clear runtime command                      | `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`.                                                                        | Pass   |
| Dockerfile runs as a non-root user                              | `Dockerfile` defines `USER app`; image inspection also showed `User=app`.                                                                        | Pass   |
| Dockerfile does not copy obvious secrets                        | The Dockerfile copies only `backend/requirements.txt`, the builder virtual environment, and `backend/app`; no `.env` copy instruction was found. | Pass   |
| `.dockerignore` excludes local secrets and non-source artifacts | `.dockerignore` includes `.git`, `.env`, `.env.*`, `venv/`, `.venv/`, `__pycache__/`, and `.pytest_cache/`.                                      | Pass   |


### B2.2 Local Image and Runtime Evidence


| Check                                      | Command or observed evidence                                                                                                                                                                                         | Result |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| Local image exists                         | `docker images task-tracker-end:dev` showed repository `task-tracker-end`, tag `dev`, image ID `74446ddc3734`, size `268MB`.                                                                                         | Pass   |
| Image runtime configuration                | `docker inspect task-tracker-end:dev --format "User={{.Config.User}} Cmd={{json .Config.Cmd}} ExposedPorts={{json .Config.ExposedPorts}}"` returned `User=app`, Uvicorn command, and `ExposedPorts={"8000/tcp":{}}`. | Pass   |
| Local container existed                    | `docker ps -a --filter "name=task-tracker-end-dev"` showed container `task-tracker-end-dev` using image `task-tracker-end:dev`.                                                                                      | Pass   |
| Container exited cleanly                   | Container status showed `Exited (0)`.                                                                                                                                                                                | Pass   |
| `/health` responded from the container run | `docker logs --tail 50 task-tracker-end-dev` showed multiple `GET /health HTTP/1.1" 200 OK` entries.                                                                                                                 | Pass   |
| Uvicorn started successfully               | Docker logs showed `Application startup complete` and `Uvicorn running on http://0.0.0.0:8000`.                                                                                                                      | Pass   |


### B2.3 Docker Log Review and 404 Finding

Docker log evidence:

```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:55208 - "GET /health HTTP/1.1" 200 OK
INFO:     172.17.0.1:37488 - "GET /health HTTP/1.1" 200 OK
INFO:     172.17.0.1:48076 - "GET / HTTP/1.1" 404 Not Found
INFO:     172.17.0.1:34262 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:47126 - "GET /health HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
```


| Finding                           | Reason                                                                                                                                                                                             | Suggested change                                                                                                                                                                                                                                                                   |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET /health` returned `200 OK`.  | The backend defines a `/health` route, and the Docker port mapping allowed the host to reach the containerized API.                                                                                | Continue using `/health` as the container health verification endpoint.                                                                                                                                                                                                            |
| `GET /` returned `404 Not Found`. | The backend does not define a root `/` route; the active API routes include `/health`, `/version`, and `/tasks`. The `172.17.0.1` address is Docker bridge traffic from the host to the container. | Use `http://localhost:8000/health`, `http://localhost:8000/version`, or `http://localhost:8000/docs` for manual checks. If a root landing response is desired, add a small `GET /` route in `backend/app/main.py`, but no application-code change was made for this evidence item. |


### B2.4 Troubleshooting and Log Commands


| Purpose                                   | Command                                                                    |
| ----------------------------------------- | -------------------------------------------------------------------------- |
| Show the named container if it exists     | `docker ps -a --filter "name=task-tracker-end-dev"`                        |
| Show all containers                       | `docker ps -a`                                                             |
| Inspect container state                   | `docker inspect task-tracker-end-dev --format "{{.State.Status}}"`         |
| Inspect Docker health status when running | `docker inspect task-tracker-end-dev --format "{{.State.Health.Status}}"`  |
| Check port mappings                       | `docker port task-tracker-end-dev`                                         |
| Print recent logs                         | `docker logs --tail 50 task-tracker-end-dev`                               |
| Follow live logs                          | `docker logs -f task-tracker-end-dev`                                      |
| Save all logs to an evidence file         | `docker logs task-tracker-end-dev *> docker-local-run.log`                 |
| Save the last 100 log lines               | `docker logs --tail 100 task-tracker-end-dev *> docker-local-run-tail.log` |


### B2.5 Docker Safety Log

```text
Non-root runtime user: PASS - Dockerfile and image configuration use app.
Slim pinned base image: PASS - Dockerfile uses python:3.11-slim, not python:latest.
No baked secrets: PASS - .dockerignore excludes .env files and Dockerfile does not copy secrets.
```

# B3. Documentation Claim Audit

Review date: 2026-08-23.

Related technical note for Docker design and documentation claim context: [technical-note.md](technical-note.md).


| Claim checked                                                                                                                                      | Evidence used                                                                                                                                                                                                                                                                                            | Result                                                                                                                                                                               | Change made, if any                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `backend/app/main.py` docstring says the app defines `/health` and CRUD routes will be wired later through `app/routes.py`.                        | `backend/app/main.py` currently defines `/health`, `/version`, `GET /tasks`, `GET /tasks/{task_id}`, `POST /tasks`, `PATCH /tasks/{task_id}`, and `DELETE /tasks/{task_id}` directly in the same file.                                                                                                   | **Concern: docstring is stale and may mislead reviewers about where active routes live.**                                                                                            | No code change made. Documented as a follow-up docstring correction.                                                                     |
| `backend/app/schemas.py` docstring says it currently defines only the `/health` response shape and that CRUD schemas will be added later.          | `backend/app/schemas.py` defines `HealthResponse` and `VersionResponse`; task request/response models already exist in `backend/app/models.py` as `TaskCreate`, `TaskUpdate`, and `TaskResponse`.                                                                                                        | **Concern: docstring is stale and should be updated if docstrings are included in final review.**                                                                                    | No code change made. Documented as a follow-up docstring correction.                                                                     |
| README status workflow claim: `ToDo -> InProgress`, `InProgress -> Done`, `Done -> InProgress`.                                                    | `backend/app/business_rules.py` defines those exact PATCH transitions and allows same-status no-op updates; `backend/app/main.py` calls `validate_status_transition()` only during PATCH when `status` is supplied.                                                                                      | Pass with clarification: accurate for PATCH status updates, but task creation can still supply any valid status enum.                                                                | No code change made. Suggested documentation wording: call this the PATCH status workflow.                                               |
| Claims that `POST /tasks` returns HTTP `201` and `DELETE /tasks/{task_id}` returns HTTP `204`.                                                     | `backend/app/main.py` sets `status_code=status.HTTP_201_CREATED` on `POST /tasks` and `status_code=status.HTTP_204_NO_CONTENT` on `DELETE /tasks/{task_id}`. Generated OpenAPI also listed POST responses `201, 422` and DELETE responses `204, 422`.                                                    | Pass.                                                                                                                                                                                | None. Keep this as verified evidence.                                                                                                    |
| Claims that validation failures return HTTP `422`.                                                                                                 | `backend/app/models.py` uses Pydantic validators and `ConfigDict(extra="forbid")`; `backend/app/business_rules.py` raises `HTTP_422_UNPROCESSABLE_ENTITY` for invalid status transitions. Tests cover missing/blank title, invalid priority, unknown fields, invalid due dates, and invalid transitions. | Pass for general 422 behavior. Exact response body text should only be quoted when captured from tests or runtime output.                                                            | None. Keep the general 422 claim and avoid uncaptured exact error-body claims.                                                           |
| Request/response schema names shown through FastAPI docs.                                                                                          | Generated OpenAPI from `app.openapi()` listed `TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus`, `TaskPriority`, `HealthResponse`, and `VersionResponse`. `POST /tasks` request body references `TaskCreate`; `POST /tasks` response references `TaskResponse`.                                   | Pass. Runtime `/docs` page was not separately inspected because no `/docs` details were pasted.                                                                                      | None. Keep OpenAPI output as schema evidence.                                                                                            |
| README says all commands are copy-pasteable from the repository root, including `backend\venv\Scripts\python.exe -m pytest -v` without activation. | Running that exact command from the repository root failed with `ModuleNotFoundError: No module named 'app'`. Running `.\venv\Scripts\python.exe -m pytest -v` from `backend` passed with `48 passed in 0.78s`.                                                                                          | **Concern: the no-activation pytest command is not reliable from the repository root in the current local environment.**                                                             | No file change made here beyond recording evidence. Suggested README change: make the no-activation command change into `backend` first. |
| README Python prerequisite says Python 3.11 is the supported course target.                                                                        | `.github/workflows/ci.yml` and `Dockerfile` use Python 3.11. The local virtual environment used during this audit reported Python 3.13.14 while still passing tests from `backend`.                                                                                                                      | **Needs verification: CI and Docker prove Python 3.11; local evidence also shows the suite can pass on this Python 3.13 environment, but 3.13 is not the documented course target.** | No change made. Keep Python 3.11 as the confirmed course/runtime target unless broader version support is intentionally documented.      |
| Docker run evidence claims `/health` returns HTTP `200`.                                                                                           | `Dockerfile` defines a health check against `http://127.0.0.1:8000/health`; Docker logs in B2 show `GET /health HTTP/1.1" 200 OK`.                                                                                                                                                                       | Pass.                                                                                                                                                                                | None. Keep the Docker `/health` evidence in B2.                                                                                          |

