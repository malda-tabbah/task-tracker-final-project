# Docker Image Creation and Local Run Procedure

## Purpose

This document records how to create and run the local Docker image for the end-course Task Tracker backend.

## Docker Role

Docker provides a repeatable local runtime for the backend API by packaging the FastAPI application, Python 3.11 runtime, and backend dependencies into a local image. In this project, the Docker image runs the backend only; the frontend is not containerized.

## Names Used

| Item | Name |
| --- | --- |
| Local image | `task-tracker-end:dev` |
| Local container | `task-tracker-end-dev` |

## 1. Build the Local Image

Run from the repository root:

```powershell
docker build -t task-tracker-end:dev .
```

Purpose:

```text
Builds the backend Docker image from the root-level Dockerfile.
```

Observed local image:

```text
Repository: task-tracker-end
Tag: dev
Image ID: 74446ddc3734
Size: 268MB
```

## 2. Run the Container Locally

Run from the repository root:

```powershell
docker run --rm --name task-tracker-end-dev -p 8000:8000 task-tracker-end:dev
```

Purpose:

```text
Starts the backend container and maps container port 8000 to host port 8000.
```

Expected startup evidence:

```text
Uvicorn running on http://0.0.0.0:8000
Application startup complete.
```

## 3. Stop the Container

If the container is running in the foreground, stop it with:

```text
Ctrl+C
```

If it is running in the background, stop it with:

```powershell
docker stop task-tracker-end-dev
```
