# Security Review

## AI Findings


| ID    | Severity | File / location                                                                                                                             | Finding                                                                                                                                       | Evidence                                                                                                                                                                                     | Suggested next step                                                                                                      | Confidence | Grade | Reason                                                                                                                                                                 |
| ----- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TT-01 | Medium   | `README.md:173`, `backend/app/main.py:82`, `backend/app/main.py:112`, `backend/app/main.py:117`                                             | All task endpoints are unauthenticated; this is intentional course scope, but it is a security gap if the API is exposed beyond local use.    | README says all endpoints are open by design; CRUD handlers are declared directly without authentication or security dependencies.                                                           | Keep local-only, or get explicit approval before adding authentication/authorization if this moves beyond course scope.  | High       | Valid | The absence of authentication is intentional for the course project, but it is a real security limitation if the API is exposed outside the local-only trust boundary. |
| TT-02 | Low      | `backend/app/main.py:34`, `backend/app/main.py:38`, `backend/app/main.py:40`, `frontend/index.html:573`                                     | CORS is broad for a local app, including `"null"` origin plus wildcard methods/headers, while the frontend hardcodes `http://localhost:8000`. | `allow_origins` includes localhost variants and `"null"`; `allow_methods` and `allow_headers` are `"*"`.                                                                                     | For non-local use, remove `"null"`, restrict methods/headers, and make the frontend API URL configurable.                | High       | Valid | This is a low-severity local-development issue because credentials are disabled, but `"null"` unnecessarily broadens the browser-side trust boundary.                  |
| TT-03 | Low      | `backend/app/models.py:23`, `backend/app/models.py:24`, `backend/app/models.py:27`, `backend/app/storage.py:8`, `backend/app/storage.py:47` | Some user-controlled strings and task volume are unbounded.                                                                                   | `title` has trimming and a 200-character limit, but `description` and `assignee` have no visible maximum length; tasks are appended to an in-memory `_tasks` dictionary with no visible cap. | Add `max_length` constraints for text fields and consider size/rate limits if the API is reachable by untrusted clients. | High       | Valid | This is a practical resource-abuse risk only if the local-only boundary is violated; within the course scope it is best handled as backlog hardening.                  |
| TT-04 | Low      | `Dockerfile:42`, `README.md:117`, `README.md:173`                                                                                           | Docker/local run instructions can expose the unauthenticated API on the host network.                                                         | Docker starts Uvicorn with `--host 0.0.0.0`; README uses `docker run --rm -p 8000:8000`; endpoints are open by design.                                                                       | Document local-only use clearly, or use `-p 127.0.0.1:8000:8000` when publishing locally.                                | High       | Valid | This is the main boundary-control issue: Docker can make the intentionally unauthenticated local API reachable beyond the intended local-only context.                 |




## My Findings

TT-04 can make the API reachable, TT-01 allows unauthorized API access once reachable, and TT-03 can increase the impact through resource exhaustion or denial of service. TT-02 is related but separate: it unnecessarily broadens the browser-side trust boundary through CORS.

### TT-01: No authentication on task endpoints

The vulnerability is that task CRUD endpoints have no authentication or authorization. This is an intentional course-scope decision, not an application bug by itself.

A realistic breach scenario is that the API is accidentally exposed on a network, allowing another user or attacker to list, create, update, or delete tasks without credentials.

The worst credible consequence is unauthorized access and loss of control over task data.

The minimum action is to document that the API is local-only and must not be externally exposed unless authentication is added.

Backlog remediation is to add authentication and authorization before any real deployment or shared-network use.

### TT-02: Broad CORS configuration includes `"null"`

The vulnerability is that the CORS allowlist includes `"null"`, with wildcard methods and headers.

A realistic breach scenario is that a local file or sandboxed origin is able to make browser-based requests to the local API in situations where only the known local frontend should be trusted.

The worst credible consequence is expanded browser-side access to an already unauthenticated local API.

The minimum action is to remove `"null"` from `allow_origins` if direct `file://` frontend usage is not required.

Backlog remediation is to make CORS environment-specific and restrict allowed methods and headers if the app moves beyond local development.

### TT-03: Unbounded strings and task growth

The vulnerability is that `description` and `assignee` do not have explicit maximum lengths, and task creation stores data in memory without a visible task-count limit.

A realistic breach scenario is that an attacker who can reach the API submits very large fields or many tasks.

The worst credible consequence is memory pressure or denial of service for the local API process.

The minimum action is to add backlog work for basic input-length limits.

Backlog remediation is to add maximum lengths for `description` and `assignee`, and consider lightweight payload-size or task-count protection before any external exposure.

### TT-04: Docker guidance exposes port 8000 beyond [localhost](http://localhost)

The vulnerability is that the Docker run guidance maps container port 8000 to the host without explicitly binding to `127.0.0.1`.

A realistic breach scenario is that a developer runs the documented Docker command on a machine connected to an untrusted network, making the unauthenticated API reachable from outside the machine.

The worst credible consequence is unauthorized API access, including viewing, changing, or deleting tasks.

The minimum action is to update documentation to bind Docker to localhost with `127.0.0.1:8000:8000`.

Backlog remediation is to keep Docker/local run guidance aligned with the local-only trust boundary and require authentication before any external deployment.


| Rank | Finding                                                       | Severity | Owner                         | Next Step                                                                                                                          |
| ---- | ------------------------------------------------------------- | -------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1    | TT-04 + TT-01: Docker can expose an unauthenticated local API | Medium   | DevOps / course-project owner | Document local-only use and change Docker guidance to bind `127.0.0.1:8000:8000`; require authentication before external exposure. |
| 2    | TT-02: `"null"` CORS origin broadens browser-side access      | Low      | Backend                       | Remove `"null"` from `allow_origins` if direct `file://` frontend use is not required.                                             |
| 3    | TT-03: Unbounded text fields and in-memory task growth        | Low      | Backend                       | Add backlog item for max lengths on `description` and `assignee`, plus lightweight resource limits before external exposure.       |


