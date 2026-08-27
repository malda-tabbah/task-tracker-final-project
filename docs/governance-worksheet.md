# Governance Retrospective AI-Assisted Coding

## What I shared with AI

| Item | Module | Risk Level | Reason | Safer future practice |
| --- | --- | --- | --- | --- |
| Task Tracker Code | 2-5 | Low | This was course toy-project code with no visible secrets, PII, production data, or proprietary business logic. | Share only the files needed for the specific task and keep `.env`, local credentials, and unrelated machine context out of prompts. |
| Test Output and stack traces | 2-4 | Medium | Test output and stack traces can reveal local paths, implementation details, dependency versions, and error behavior even when they do not contain secrets. | Trim logs to the relevant error lines and review them for secrets, tokens, usernames, or private paths before sharing. |
| Front end Code | 3 | Low | The frontend was course-project HTML/CSS/JavaScript and did not contain visible secrets or sensitive user data. | Share only relevant snippets or files and avoid including real API keys, analytics IDs, user data, or production endpoints. |
| Docker File and CI YAML | 4 | Low | The Dockerfile and CI workflow described local build/test behavior and did not contain visible credentials or deployment secrets. | Continue keeping secrets in protected environment variables and review workflow files before sharing them outside the course context. |
| Any other external data | used by mistake | High | Accidental external data has unknown sensitivity and may include information I was not authorized to share. | Verify ownership and sensitivity before sharing, redact unnecessary data, and avoid uploading third-party or real-world data unless explicitly permitted. |
