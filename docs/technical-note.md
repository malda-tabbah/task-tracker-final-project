# Dockerfile Design for Local Containerized Runs

## 1. Context

Before this decision, the Task Tracker ran only as a bare Python process: `README.md`'s "Run the app locally" section documents starting the API with `uvicorn app.main:app --reload --port 8000` from inside a `backend/venv` virtual environment, with dependencies installed from `backend/requirements.txt`. There was no container image, no `Dockerfile`, and no `.dockerignore` — anyone running the project needed a local Python 3.11 install and manual virtualenv setup (`README.md` "Local setup", steps 1–2).

`backend/app/main.py` already exposed a `/health` liveness endpoint (`health_check()`, returning `HealthResponse(status="ok", timestamp=...)`) and read `APP_ENV` via `os.getenv("APP_ENV", "development")`, using `backend/.env` locally. `CLAUDE.md`'s "Do Not" list constrains the project (no authentication, no database without asking, no response-shape changes without approval) but does not prohibit packaging. `.github/workflows/ci.yml` ran `pytest -v` against `backend/` on `ubuntu-latest` with no image-building step of any kind.

## 2. Decision

Add a multi-stage `Dockerfile` at the repo root (`builder` stage installs dependencies into a venv from `backend/requirements.txt`; `runtime` stage copies that venv plus `backend/app` into a `python:3.11-slim` image, runs as a non-root `app` user, and starts `uvicorn app.main:app --host 0.0.0.0 --port 8000`), paired with a root-level `.dockerignore` — for local containerized runs only, not production deployment.

## 3. Alternatives Considered

- **Single-stage Dockerfile.** Installing `backend/requirements.txt` with `pip install` directly in one `python:3.11-slim` stage was rejected because it would leave `pip`'s build/cache artifacts in the final image layers; the `builder`/`runtime` split in the current `Dockerfile` (lines 6–19) keeps only the installed `/opt/venv` and `backend/app` in the shipped image.
- **Copying `backend/.env` into the image.** Baking the local `.env` file into the image so `APP_ENV` and other settings travel with it was rejected in favor of excluding it via `.dockerignore` (`.env`, `.env.*`) and passing `APP_ENV` at run time instead (`README.md`'s Docker notes: `docker run --rm -p 8000:8000 -e APP_ENV=development task-tracker`). This avoids committing environment-specific values into image layers.
- **Containerizing the frontend alongside the backend.** A single image (or `docker-compose` setup) serving both `frontend/index.html` and the API was rejected; `README.md`'s "Run with Docker" section states explicitly "The frontend is not containerized; run it separately," keeping the `Dockerfile` scoped to the FastAPI backend only.

## 4. Trade-offs

- The `builder`/`runtime` split makes the `Dockerfile` longer and requires understanding multi-stage `COPY --from=builder` semantics, versus a simpler (if heavier) single-stage file — added authoring/maintenance complexity in exchange for a smaller runtime image.
- `.dockerignore` excludes `tests/` and `docs/` from the build context, so the container itself never runs `pytest`; a successful `docker build` says nothing about whether the test suite passes — verification still depends entirely on `.github/workflows/ci.yml` running outside the image.
- The `HEALTHCHECK` (lines 37–38) shells out to Python's `urllib.request` against `/health` instead of `curl`/`wget`, avoiding adding an extra package to the slim image, but ties the health check to the app's own Python environment rather than a standalone tool.
- Running as the non-root `app` user (`groupadd --gid 1000 app`, `useradd --uid 1000 ...`) is safer but means any future feature needing to write outside `/app` (e.g., a mounted volume) would need explicit ownership handling — not needed today since storage is in-memory only, but a constraint the current design accepts up front.

## 5. Consequences

- `.github/workflows/ci.yml` never builds or runs the `Dockerfile` — `README.md`'s own "CI workflow summary" states "No linting, coverage, Docker build, or deploy steps are currently part of CI" — so a change that breaks the image (e.g., a `backend/requirements.txt` edit incompatible with `python:3.11-slim`) would not be caught until someone runs `docker build` manually.
- `.dockerignore` keeps `docs/`, `CLAUDE.md`, `.github`, and `tests/` out of the build context and the final image, reducing image size and keeping internal project documentation out of any distributed image.
- Because the image only runs the backend and `APP_ENV` defaults to `development` unless overridden, the container's runtime behavior mirrors local `uvicorn` runs closely, but only for the API — there is no single command that brings up API + frontend together in containers.

## 6. Open Questions

- Should `.github/workflows/ci.yml` add a step to build the `Dockerfile` (and optionally curl `/health` against the running container) so image breakage is caught in CI, given it currently does neither?
- `README.md`'s Prerequisites section marks the Python 3.11 requirement as `[VERIFY]` ("earlier 3.x versions are not verified to work"); since `python:3.11-slim` in the `Dockerfile` is the only place that version is actually enforced rather than just stated, should the `Dockerfile` be treated as the source of truth for the supported Python version?
- If a future change needs the API and frontend running together via containers, should that be a `docker-compose.yml` addition, or does the "frontend is not containerized" stance in `README.md` remain a deliberate boundary for this project's scope?
