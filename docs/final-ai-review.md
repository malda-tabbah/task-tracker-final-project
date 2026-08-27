# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| README no-activation pytest command fails from repo root. | Useful | The README says commands are copy-pasteable from the repository root, but this command needs the backend working directory for `app` imports. | Verified by running the root command, which failed with `ModuleNotFoundError`; running pytest from `backend` passed. Fix README command. |
| Docker run command uses `-p 8000:8000`, which may expose the unauthenticated API beyond localhost. | Useful | The project is documented as local-only and unauthenticated, so Docker guidance should preserve that boundary. | Verified from the README Docker command and Dockerfile Uvicorn host `0.0.0.0`. Prefer `-p 127.0.0.1:8000:8000` or document the exposure. |
| CI evidence links in `release-evidence.md` are malformed or rendered as code. | Useful | Broken evidence links make release documentation harder to verify. | Verified in `docs/endcourse/release-evidence.md`. Fix Markdown link syntax. |
| Workflow safety table has an orphan `true present` row. | Useful | The row makes the `continue-on-error` check unclear. | Verified in `docs/endcourse/release-evidence.md`; `.github/workflows/ci.yml` has no `continue-on-error`. Remove or correct the row. |
| Technical note references stale README Docker command/image name. | Useful | The technical note no longer matches the current README Docker instructions. | Verified: `technical-note.md` mentions `task-tracker`, while README uses `task-tracker-end:dev`. Update the note. |

## AI security mini-review

Detailed security review: [security-review.md](security-review.md).

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Task endpoints are unauthenticated. | `README.md` documents no authentication; task routes in `backend/app/main.py` have no auth dependency. | Valid | This is intentional course scope, but would be unsafe if exposed beyond local use. | Keep documented as local-only; add authentication before any real deployment. |
| Docker command can expose the unauthenticated API beyond localhost. | README Docker command uses `-p 8000:8000`; Dockerfile runs Uvicorn on `0.0.0.0`. | Valid | The API is local-only and unauthenticated, so the binding matters. | Prefer `-p 127.0.0.1:8000:8000` in docs or clearly warn about exposure. |
| CORS includes `"null"` with broad methods and headers. | `backend/app/main.py` configures CORS origins and wildcard methods/headers. | Valid | This broadens browser-side access for a local unauthenticated API. | Keep as known local-dev limitation or remove `"null"` if file-origin frontend use is not needed. |
| Some user-controlled fields and in-memory task volume are not tightly bounded. | `backend/app/models.py` limits title but not description/assignee; `backend/app/storage.py` stores tasks in memory. | Valid | This is low risk for a local course app, but could become a resource issue if exposed. | Add backlog item for field length limits and basic resource controls before external use. |

## Manual security check

Related technical note: [technical-note.md](technical-note.md).

I checked the README, Dockerfile, `.dockerignore`, CI workflow, backend route definitions, model validation, storage layer, and security documentation myself. I found that the project is intentionally local-only, has no authentication, stores tasks in memory, and does not include secrets in the Docker image. This matters because the main security boundary is not application login or database protection; it is keeping the service local and avoiding accidental exposure.

## One AI output I rejected or corrected

AI identified several documentation and security concerns, but I did not accept them blindly as code changes. For example, the Docker localhost-binding comment was valid, but I treated it as a documentation/safety guidance issue rather than immediately changing application code. I verified the claim against the README and Dockerfile first, then recorded the minimal next action.

## Three AI usage rules

1. Never paste: secrets, `.env` values, credentials, tokens, private repository settings, or unrelated local machine data.
2. Always verify: AI claims against the actual repo files, test output, CI logs, Docker behavior, or manual runtime checks before accepting them.
3. Record AI contributions by: keeping review logs, noting which suggestions were accepted or rejected, and documenting the verification evidence used.

## Ownership statement

I am comfortable submitting this repository as my work because I reviewed the AI suggestions instead of accepting them automatically. The final project scope, commands, tests, Docker behavior, and security limitations were checked against the actual repository files. I understand the main design choices: this is a local learning project with in-memory storage, no authentication, and backend-only Docker packaging. AI helped with review and documentation, but I made the final decisions about what evidence to keep and what changes belong in scope.
