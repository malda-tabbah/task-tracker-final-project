# Part A - Baseline Preparation and Check

## A1. Creating and Verifying the End Project Baseline

Review date: 2026-08-23 (original End-Course baseline).  
Rechecked against the restructured public repository on 2026-08-28.

Baseline preparation evidence is documented in
[prepare_end_baseline.md](prepare_end_baseline.md). That procedure records the
original End-Course baseline preparation, including the earlier working copy,
development branch, and initial public End-Course repository.

Following review feedback, the public submission was reorganized into the
current repository:
[task-tracker-final-project](https://github.com/malda-tabbah/task-tracker-final-project).

### Current Repository Baseline

- Local working copy: `C:\_Malda\Projects\task-tracker - end-project`.
- Current public remote: `final-public`.
- Public repository: `task-tracker-final-project`.
- Public branches:
  - `mid-course-project` at `e5772bd` (`Document PATCH title validation fix and testing`).
  - `final-project` at `aa1a215` (`Update final project documentation and repository structure`).
- `mid-course-project` preserves the corrected Mid-Course baseline, including
the review fixes and PATCH title-validation regression tests.
- `final-project` was created from the corrected Mid-Course baseline and
contains the Final Project and End-Course deliverables.
- The public branch state was verified using
`git ls-remote --heads final-public`.

**Result:** The corrected Mid-Course project is preserved independently on
`mid-course-project`, while the Final Project is published on `final-project`
in the current `task-tracker-final-project` public repository. This establishes
the corrected Mid-Course state as the baseline from which the Final Project
submission was built.

## A2. Verifying Successful Baseline Testing



## A2. Verifying Successful Baseline Testing

Original verification date: 2026-08-23.  
Re-verification after Mid-Course corrections and repository restructuring:
2026-08-27 to 2026-08-28.

The original baseline service health and test procedure is documented in
[service-health-check.md](service-health-check.md).

### Original Baseline Verification

Before the repository restructuring:

- Backend API startup and `GET /health` were verified successfully.
- Frontend access was verified by opening `http://localhost:5500/` and
confirming that the Kanban board and create/edit flow were operational.
- The full backend pytest suite passed with `48 passed in 1.01s`.



### Current Baseline Re-verification

Following the Mid-Course review corrections and creation of the current
`mid-course-project` and `final-project` branch structure, the project was
re-tested from the current working copy.

- The complete backend pytest suite passed with `51 passed in 2.32s`.
- The additional tests include regression coverage for explicit `null`,
blank, and empty titles in PATCH requests.
- Docker image `task-tracker-final:dev` built successfully.
- Container `task-tracker-final-dev` started successfully and reported healthy.
- `GET /health` returned `200 OK`.
- `GET /version` returned `200 OK` with application version `0.1.1`.
- GitHub Actions CI completed successfully for the `final-project` branch in
the current `task-tracker-final-project` public repository.

**Result:** The corrected baseline remained functional after the Mid-Course
review changes and repository restructuring. The expanded 51-test regression
suite, Docker runtime checks, API health/version checks, and successful CI run
provide the verified baseline for the Final Project.

## Final Submission Repository Structure

The end-course development and verification activities documented below were
originally performed using the `end-course-project` branch/repository.

Following review feedback, the final public submission was reorganized into
`task-tracker-final-project` with two branches:

- `mid-course-project` — corrected Mid-Course project and review fixes.
- `final-project` — Final Project built from the corrected Mid-Course baseline
and containing the End-Course deliverables.

References below to `end-course-project`, `origin/end-course-project`, and the
original End-Course GitHub Actions runs are retained as historical evidence of
the development and verification process.

# Part B - Release Readiness Evidence



## B1. CI Workflow



### B1.1 Workflow Verification

The `CI` workflow is triggered on every `push` and every `pull_request`. Once triggered, it runs on `ubuntu-latest`, sets up Python 3.11, installs the backend dependencies from `backend/requirements.txt`, and runs the backend test suite with `pytest -v` from the `backend` directory.

- Workflow: `[CI](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33120225711)`, defined in `.github/workflows/ci.yml`.
- Trigger: push to `final-project`.
- Pushed commit: `aa1a21563d82f2ba9d010915a3fa9de6206e7cd7` (`Update final project documentation and repository structure`).
- Workflow run: `CI` run 3, created at `2026-08-27T21:54Z` and completed successfully (total duration 14s).
- Test job: `[test](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33120225711/job/98684983625)`, completed successfully in 10s.
- CI pytest result: the job log is not publicly visible without GitHub sign-in; the `test` job succeeded. The suite at this commit contains 51 tests (`test_tasks.py` 22, `test_overdue.py` 12, `test_due_date.py` 10, `test_search_filter.py` 7). The earlier `48 passed in 0.27s` figure was from the old `task-tracker` run 10 and does not apply to this run.
- Earlier public-repository workflow evidence is also recorded in [service-health-check.md](service-health-check.md), including public `CI` run 2 on `main`, which completed successfully for commit `94d00568c21c2758745c8b05a8ac26e11924d8d3`.



### B1.2 Workflow Safety Review

Review date: 2026-08-28.  
Reviewed branch: `final-project` at `f50b631`.  
Public repository: [task-tracker-final-project](https://github.com/malda-tabbah/task-tracker-final-project).  
Source of truth: `.github/workflows/ci.yml` in the current working copy, with `backend/requirements.txt` and `backend/pytest.ini` inspected for referenced install and test behavior.

This review is a local configuration check of the Final Project workflow. It does not reuse End-Course B1.2 findings. Live GitHub Actions job logs for this commit were not re-opened as part of this check.

| Check | Pass/Concern | Current Repository Evidence | Required Action |
| ------------------------------------------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| Both `push` and `pull_request` triggers | Pass | `.github/workflows/ci.yml` `on:` defines `push:` and `pull_request:`. | None. |
| Python version | Pass | `actions/setup-python@v5` with `python-version: "3.11"`. | None. |
| Backend dependencies installed | Pass | `pip install -r requirements.txt` runs with `defaults.run.working-directory: backend`, so the file is `backend/requirements.txt` (includes `pytest==9.1.1`). | None. |
| pytest actually runs | Pass | Step `Run tests` executes `pytest -v` in `backend`. | None. |
| `continue-on-error` present | Pass | Not present in `.github/workflows/ci.yml`. | None. |
| `--exit-zero` used | Pass | Not present in the workflow or in `backend/pytest.ini`. | None. |
| Pytest output piped or wrapped | Pass | `pytest -v` is run directly with no pipe or `|| true`. | None. |
| Deployment steps in this CI workflow | Pass | Steps are checkout, Python 3.11 setup, dependency install, and pytest only. | None. |
| Workflow path `.github/workflows/ci.yml` | Pass | The workflow file is at `.github/workflows/ci.yml`. It is the only workflow under `.github/workflows/`. | None. |
| Other failure-hiding configuration | Pass | Single `test` job; no `if:` skip, `allow_failure`, or pytest `addopts` that would ignore failures. Live Actions logs: not verified in this review. | None. |

**B1.2 result:** PASS. The workflow is test-only and fail-closed on pytest failure. No workflow change is required.




### B1.3 Intentional Red-Run Evidence

Purpose: confirm that the `CI` workflow in
[task-tracker-final-project](https://github.com/malda-tabbah/task-tracker-final-project)
fails when pytest detects a failing test, then returns to green after the
intentional break is reverted.

Review date: 2026-08-28.  
Reviewed branch: `final-project`.  
This red/green pair was performed on the current public repository. Earlier
End-Course evidence from `malda-tabbah/task-tracker` (48 tests, Actions runs
12 and 13) is not used as current proof.


| Step | Evidence | Result |
| ---- | -------- | ------ |
| Local break test | Temporary file: `backend/tests/test_intentional_red_run.py`. Working directory: `backend`. Command: `.\venv\Scripts\python.exe -m pytest -v tests/test_intentional_red_run.py`. | Failed as intended: `tests/test_intentional_red_run.py::test_intentional_ci_red_run_fails`; result: `1 failed in 1.07s`. Local full suite at the same commit: `1 failed, 51 passed in 1.51s`. |
| Red CI run | Commit: `34a1a60879b2e20e40be545bb855de83b717ce72` (`Intentional CI red run`). Workflow: [CI run 4](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33185934234). Test job: [test](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33185934234/job/98898821842). | Failed as expected. Public run status: Failure. Annotation: `Process completed with exit code 1`. Job logs are not publicly visible without GitHub sign-in. |
| Revert and local green check | Revert commit: `1afaa48e93b17c030f140a7294a44b6553971e20` (`Revert "Intentional CI red run"`). The temporary failing test file was removed. Working directory: `backend`. Command: `.\venv\Scripts\python.exe -m pytest -v`. | Local full suite passed after revert: `51 passed in 2.59s`. |
| Green CI run | Workflow: [CI run 5](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33186168149). Test job: [test](https://github.com/malda-tabbah/task-tracker-final-project/actions/runs/33186168149/job/98899604055). Pushed commit: `1afaa48`. | Completed successfully. Public run status: Success (15s). Job logs are not publicly visible without GitHub sign-in. |

**B1.3 result:** PASS. The current `CI` workflow on `final-project` failed when the intentional test failed, and returned to green after the revert.




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


