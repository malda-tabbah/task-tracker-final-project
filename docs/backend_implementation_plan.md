# Backend Implementation Plan: Due Date, Overdue Logic, and Advanced Filtering

## 1. Purpose

This document is a backend-only implementation plan for the Task Tracker due-date extension (US-08 to US-11). It describes how to add `due_date`, `due_date_change_date`, dynamic overdue detection, and combined filtering/search without changing architecture, introducing a database, or implementing the work yet.

The plan maps the mini-ADR and user stories onto the **actual** backend modules in this repository. It does not invent features, routes, or transition rules beyond those documents.

This document is planning only. No backend, frontend, or test code is modified by producing it.

## 2. Source Documents Reviewed

| Document | Path | Role |
| --- | --- | --- |
| Mini-ADR addendum | `docs/mini-adr.md` | Architecture, data model, validation, overdue rule, filtering, risks |
| User stories | `docs/user_stories.md` | Functional scope and acceptance criteria (US-01 to US-11) |

The existing backend was also inspected so file paths in this plan match the running project, not the hypothetical folder tree in the mini-ADR.

**Actual backend (current):**

```text
backend/app/main.py              # FastAPI app, CORS, /health, /version, task CRUD routes
backend/app/models.py            # TaskStatus, TaskPriority, TaskCreate, TaskUpdate, TaskResponse
backend/app/business_rules.py    # Status transition validation only
backend/app/storage.py           # In-memory dict store; list filter by status and priority
backend/app/schemas.py           # HealthResponse, VersionResponse only
backend/tests/test_tasks.py      # Existing CRUD / filter / transition tests
backend/tests/conftest.py        # TestClient + autouse storage reset
```

There is no `api/tasks.py`, `services/task_service.py`, `storage/json_task_repository.py`, or `tasks.json` in the current tree. Routes live in `main.py`. Task request/response schemas live in `models.py`. Persistence is an in-memory `_tasks` dict that is cleared on process restart.

**Existing list filters already implemented:** `GET /tasks?status=&priority=` (logical AND). Assignee, due date, overdue, and title search are not implemented.

## 3. Implementation Principles

Preserve the current layered responsibilities. Introduce a thin service/orchestration boundary if needed so storage does not own overdue or filter business rules. Do not replace the in-memory store with a database.

```text
FastAPI routes          (backend/app/main.py)
        ↓
Pydantic schemas        (backend/app/models.py)
        ↓
Task service / rules    (backend/app/business_rules.py and/or a new thin service module)
        ↓
Storage repository      (backend/app/storage.py)
        ↓
In-memory task store    (_tasks dict)
```

This matches the mini-ADR **Decision** section (keep in-memory storage; do not introduce `tasks.json` for this extension). It does **not** match later mini-ADR diagrams that still show a JSON repository and `tasks.json`. That conflict is recorded in section 8. This plan does not introduce SQLite, SQLModel, Docker, auth, notifications, or real-time updates.

Responsibility split:

| Layer | Owns | Must not own |
| --- | --- | --- |
| Routes (`main.py`) | HTTP, query params, status codes, returning `TaskResponse` | Overdue formula, due-date change tracking, filter AND logic |
| Pydantic (`models.py`) | Request/response shape, required fields, date format, `extra="forbid"` | Computing overdue, writing `due_date_change_date` |
| Service / business rules | Status transitions (existing), due-date change tracking, overdue calculation, combined filters and title search | HTTP details, raw dict persistence |
| Storage (`storage.py`) | Create, read, update, delete of stored task records | Overdue flag, client validation, status workflow |

Additional rules from the source documents:

- `overdue` is **calculated**, never stored on the task record.
- `due_date_change_date` **is stored**. It is system-generated. Clients must not set it.
- On create, `due_date_change_date` is empty/`null`. Setting the initial due date is not a change (US-08).
- Date comparison uses the **server** calendar date, not the browser date (US-09, US-10).
- Filters combine with **logical AND** (US-11). Title search is partial and case-insensitive.
- Existing status workflow stays unchanged (US-06 / `business_rules.py`).
- Frontend must not contain the core overdue rule. This plan does not include frontend work.
- Do not add authentication, user accounts, multi-tenancy, notifications, real-time updates, Docker, microservices, cloud deployment, or a production database.

Recommended stored vs response split (needed because `storage.py` currently stores `TaskResponse` objects):

- **Stored record:** existing fields plus `due_date` and `due_date_change_date`. No `overdue`.
- **API response (`TaskResponse`):** stored fields plus computed `overdue`.
- Compute `overdue` on every create, get, list, and update response so a stored `TaskResponse` cannot freeze a stale flag.

## 4. Step-by-Step Backend Implementation Plan

| Step | Backend Area | Files / Modules | Change Required | Reason | Dependencies | Validation / Tests |
| ---- | ------------ | --------------- | --------------- | ------ | ------------ | ------------------ |
| 1 | Review current backend | `backend/app/main.py`, `models.py`, `business_rules.py`, `storage.py`, `schemas.py`, `backend/tests/test_tasks.py`, `conftest.py` | Confirm routes, schemas, in-memory store, existing status/priority AND filters, and which create tests omit `due_date`. Do not change code in this step. | Implementation must extend the real modules, not the hypothetical ADR folder tree. | None | Checklist only: list endpoints, current `TaskCreate`/`TaskUpdate`/`TaskResponse` fields, `get_all_tasks` filters, fixture payloads |
| 2 | Task stored model | `backend/app/models.py`; possibly a stored-record type if `TaskResponse` is split | Add stored fields `due_date: date` and `due_date_change_date: date \| None`. Do not add stored `overdue`. Keep `id`, `title`, `description`, `status`, `priority`, `assignee`, `created_at`, `updated_at`. | US-08/US-09 require both date fields on the task; mini-ADR says overdue is not stored. | Step 1 | Model/unit tests that a stored task can hold both date fields and omit `overdue` |
| 3 | Pydantic request and response schemas | `backend/app/models.py` (`TaskCreate`, `TaskUpdate`, `TaskResponse`) | `TaskCreate`: required `due_date: date`. Do not include `due_date_change_date` or `overdue`. `TaskUpdate`: optional `due_date: date`. Do not include `due_date_change_date` or `overdue`. `TaskResponse`: add `due_date`, `due_date_change_date`, and computed `overdue: bool`. Keep `extra="forbid"` on all three. | Create must require due date (US-08 AC4). Update may change due date (US-09). Response must show dates and overdue (US-08, US-10). | Step 2 | Schema tests: valid ISO date accepted; missing due date on create → 422; unknown fields still 422 |
| 4 | Due date validation | `backend/app/models.py` | Use Pydantic `datetime.date` so values must be valid calendar dates (JSON `YYYY-MM-DD`). Invalid strings, empty strings, and non-dates return 422. Do not add extra range rules (no “must be future”) — none are specified. | US-08 AC3 and US-09 AC4 reject invalid due dates. Mini-ADR: valid date format required. | Step 3 | `test_due_date.py`: invalid format, empty string, non-date types → 422; valid date stored |
| 5 | Prevent manual `due_date_change_date` | `backend/app/models.py` (`TaskCreate`, `TaskUpdate`) | Do not declare `due_date_change_date` (or `overdue`) on request models. With `extra="forbid"`, a client-supplied `due_date_change_date` is rejected as an unknown field (422). Do not copy any client value into storage even if a future schema change adds the field. | US-09 notes: system-generated, cannot be manually supplied. Mini-ADR: reject or ignore client-supplied change date and overdue. | Step 3 | `test_due_date_change.py`: POST/PATCH with `due_date_change_date` → 422; stored value unchanged on PATCH of other fields |
| 6 | Create task logic | `backend/app/storage.py` `add_task`; `backend/app/main.py` `create_task`; optional service wrapper | Persist required `due_date` from `TaskCreate`. Set `due_date_change_date` to `null`. Do not treat initial due date as a change (US-08 AC5 / notes). Attach computed `overdue` only on the response. | New tasks must store due date and leave change date empty. | Steps 3–5 | `test_due_date.py`: create with due date → 201, field stored, `due_date_change_date` is null; create without due date → 422 |
| 7 | Task update logic | `backend/app/storage.py` `update_task`; `backend/app/main.py` `update_task`; `business_rules.py` (existing transition check stays) | Continue partial PATCH. If `due_date` is omitted, leave both date fields unchanged. If `due_date` is present but invalid, Pydantic rejects before storage (neither date field changes). If task id is missing, keep 404. Do not change US-06 transition behavior. | US-09 AC1, AC4, AC5; US-05/US-06 still apply. | Steps 3–4, existing `validate_status_transition` | Existing transition tests plus due-date update tests; invalid due date leaves previous dates intact |
| 8 | Automatic due date change tracking | `backend/app/business_rules.py` or thin service used by update | After a valid PATCH, compare previous stored `due_date` with the new value. Only if they differ, set `due_date_change_date` to the current **server** date. Same due date or updates to title/description/status/priority/assignee must not change `due_date_change_date`. | US-09 AC2–AC3. Mini-ADR: compare old vs new before updating the change date. | Steps 6–7; server-date helper (step 9) | `test_due_date_change.py`: change due date updates change date; other-field PATCH does not; same-date PATCH does not |
| 9 | Overdue calculation | `backend/app/business_rules.py` and optionally `backend/app/utils/date_utils.py` | Add a single helper, e.g. `is_overdue(due_date, status, today) -> bool`. Rule: `due_date < current_server_date` AND `status in {ToDo, InProgress}`. Otherwise false: due date is today, due date is future, status is Done, or due date is missing on a legacy record. Use one `current_server_date()` helper so tests can freeze “today”. Do not persist the result. | US-10 AC1, AC2, AC5. Mini-ADR overdue rule uses `<`, not `<=`. | Steps 2–3 | `test_overdue.py`: past + ToDo/InProgress → true; today → false; future → false; Done + past → false; missing due date → false |
| 10 | Include overdue on list/get/create/update responses | `TaskResponse`; mapping function used by routes/service | Every successful task response includes `overdue` computed at read time. List, get-by-id, create, and patch all use the same mapper. Done tasks return `overdue: false` (see section 8 for US-10 AC4 wording). | Callers must see overdue without storing it. Mini-ADR response example includes `overdue`. | Steps 2, 9 | Assert `overdue` present on GET/POST/PATCH; Done task has `overdue` false |
| 11 | Extend filtering | `backend/app/main.py` `list_tasks` query params; service or `storage.py` filter function | Add optional query params: `due_date` (exact date match), `overdue` (bool), `assignee` (exact match, same style as current status/priority). Keep existing `status` and `priority`. Unknown enum/date values still 422 via FastAPI/Pydantic. | US-11 AC1–AC3; mini-ADR `get_tasks(...)`. Current AND filters for status/priority should be reused, not replaced. | Steps 9–10 (overdue must be computed before overdue filter) | `test_search_filter.py`: each filter alone; no match → 200 and `[]` |
| 12 | Title / name search | Same list path as step 11 | Add optional query param `title` (task name). Match if the search string is a substring of `task.title`, case-insensitive. Do not add a separate `name` field. | US-11 AC4 and notes: partial, case-insensitive title search. | Step 11 | Search `"prep"` matches `"Prepare sprint review"`; different case matches; no match → `[]` |
| 13 | Combined filters (logical AND) | Service-layer filter function | Apply every supplied filter. A task is returned only if it satisfies all of: status, priority, assignee, due date, overdue flag, and title search (each applied only when that param is present). Suggested order from mini-ADR: load → normalize → compute overdue → AND filters → title search. Clearing a param (omit it) means “no constraint,” which already matches US-03/US-04. | US-11 notes: multiple filters use logical AND. | Steps 11–12 | Combination tests: e.g. status + overdue + title; mismatch on one dimension excludes the task |
| 14 | Legacy records missing due date fields | `storage.py` read path and/or a normalize helper | When reading a stored record, default missing `due_date_change_date` to `null`. If `due_date` is missing, do not invent a date; treat as not overdue (mini-ADR overdue exceptions). New creates still require `due_date`. In the current in-memory store this mainly protects tests, `--reload` edge cases, and any later persistence format. If JSON persistence were added later, run the same normalize-on-read against file records. Do not write a database migration. | Mini-ADR: older stored tasks may lack `due_date`; handle safely. US-10 AC3 says missing due date is not possible — conflict in section 8. | Steps 2, 9 | Unit test: record without `due_date` lists without crashing and `overdue` is false |
| 15 | Backend tests | `backend/tests/conftest.py`, `test_tasks.py`; add `test_due_date.py`, `test_due_date_change.py`, `test_overdue.py`, `test_search_filter.py` | Update `created_task` and existing POST bodies to include a valid `due_date` so current tests keep passing. Extend expected response keys with `due_date`, `due_date_change_date`, `overdue`. Add the new files for extension scenarios in section 5. Keep using in-memory `_reset()` (do not switch tests to a real `tasks.json` unless storage itself changes). | Mini-ADR test list; existing suite will 422 on create once due date is required. | Steps 3–13 | New tests plus updated regression tests all collected by pytest |
| 16 | Validation and regression | `backend/` with venv | Run `pytest -v`. Confirm US-06 transition tests, existing status/priority filters, CRUD, and new due-date/overdue/filter tests all pass. Fix regressions before considering the backend slice done. | Required existing behavior must not break (US-01 to US-07 plus new US-08 to US-11). | Step 15 | Full suite green; no production database, Docker, or CI work |

Optional supporting step (only if date/filter logic makes `business_rules.py` hard to read): add `backend/app/utils/date_utils.py` with `current_server_date()`, `is_overdue(...)`, and date parse/normalize helpers, as allowed by the mini-ADR. This is not required to start.

Optional structural step (only if `main.py` / `storage.py` would otherwise mix HTTP, rules, and persistence): add a thin `backend/app/service.py` (or `services/task_service.py`) that create/update/list call, while storage stays CRUD-only. Do not add auth, a JSON file, or a database as part of that extraction.

## 5. Testing Plan

Use FastAPI `TestClient` and the existing autouse storage reset. Freeze server “today” in overdue tests (patch `current_server_date()` or equivalent) so results do not depend on the developer machine’s clock.

Update `backend/tests/conftest.py` `created_task` to POST a valid `due_date`. Update `backend/tests/test_tasks.py` response-key assertions and any create payload that will otherwise fail US-08.

| Test Area | Scenario | Expected Result | Suggested Test File |
| --------- | -------- | --------------- | ------------------- |
| Create with due date | POST `/tasks` with required fields and `due_date` `"2026-08-20"` | 201; body includes `due_date`, `due_date_change_date: null`, and computed `overdue` | `backend/tests/test_due_date.py` |
| Reject create without due date | POST `/tasks` with title but no `due_date` | 422; no task stored | `backend/tests/test_due_date.py` |
| Reject invalid due date (create) | POST with `due_date` `"not-a-date"` or `"2026-13-40"` | 422; no task stored | `backend/tests/test_due_date.py` |
| Reject invalid due date (update) | PATCH existing task with invalid `due_date` | 422; previous `due_date` and `due_date_change_date` unchanged | `backend/tests/test_due_date.py` |
| Change a due date | PATCH `due_date` to a different valid date | 200; `due_date` is the new value | `backend/tests/test_due_date_change.py` |
| Update other fields without changing due date | PATCH `description` or `priority` only | 200; `due_date` and `due_date_change_date` unchanged | `backend/tests/test_due_date_change.py` |
| Automatic `due_date_change_date` | Successful due date change | `due_date_change_date` equals the frozen server date | `backend/tests/test_due_date_change.py` |
| Prevent manual `due_date_change_date` | POST or PATCH including `due_date_change_date` | 422 (`extra="forbid"`); on PATCH, stored change date unchanged | `backend/tests/test_due_date_change.py` |
| Same due date PATCH | PATCH `due_date` to the value already stored | 200; `due_date_change_date` unchanged | `backend/tests/test_due_date_change.py` |
| Overdue detection | Task due yesterday, status ToDo or InProgress | Response `overdue` is `true` | `backend/tests/test_overdue.py` |
| Done task not overdue | Task due yesterday, status Done | `overdue` is `false` | `backend/tests/test_overdue.py` |
| Due date equal to today not overdue | Task `due_date` is frozen “today”, status ToDo | `overdue` is `false` | `backend/tests/test_overdue.py` |
| Future due date not overdue | Due date after frozen today, status ToDo | `overdue` is `false` | `backend/tests/test_overdue.py` |
| Done after overdue | Overdue InProgress task patched to Done (via InProgress → Done) | After Done, `overdue` is `false` | `backend/tests/test_overdue.py` |
| Filter by due date | `GET /tasks?due_date=2026-08-20` | Only tasks with that exact due date; no match → `[]` | `backend/tests/test_search_filter.py` |
| Filter by overdue flag | `GET /tasks?overdue=true` and `overdue=false` | Only tasks whose computed flag matches | `backend/tests/test_search_filter.py` |
| Filter by status | Existing `GET /tasks?status=ToDo` still works with new fields | Only matching status; empty list when none match | `backend/tests/test_search_filter.py` and existing `test_tasks.py` |
| Filter by priority | Existing `GET /tasks?priority=High` still works | Only matching priority | `backend/tests/test_search_filter.py` and existing `test_tasks.py` |
| Filter by assignee | `GET /tasks?assignee=alice` | Only tasks with that assignee | `backend/tests/test_search_filter.py` |
| Search by task title | `GET /tasks?title=sprint` (mixed case) | Partial, case-insensitive title matches | `backend/tests/test_search_filter.py` |
| Combining multiple filters | e.g. `status=ToDo&priority=High&overdue=true&title=review` | Logical AND; a task missing any criterion is excluded; no matches → `[]` | `backend/tests/test_search_filter.py` |
| Legacy missing due date | In-memory record without `due_date` is listed | No crash; `overdue` false | `backend/tests/test_overdue.py` |
| Regression: unknown field | POST still rejects extra fields | 422 | `backend/tests/test_tasks.py` |
| Regression: status transitions | ToDo → InProgress allowed; ToDo → Done rejected; Done → ToDo rejected | Unchanged 200/422 behavior | `backend/tests/test_tasks.py` |

## 6. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| `overdue` accidentally stored on the in-memory record (current store uses `TaskResponse`) | Split stored fields from response, or always recompute `overdue` on the way out and never write it into `_tasks` |
| Client sends `due_date_change_date` or `overdue` | Omit both from request models; keep `extra="forbid"` so POST/PATCH return 422 |
| Change date updates when unrelated fields change, or when PATCH repeats the same due date | Compare previous and new `due_date`; update change date only when they differ |
| Done task still appears overdue | `is_overdue` returns false whenever status is Done, regardless of due date |
| “Today” differs across machines / UTC vs local | One `current_server_date()` helper; freeze it in tests; document that comparison uses the backend process date (see section 8) |
| Existing pytest creates omit `due_date` and will fail | Update fixtures and old POST bodies in the same backend change set as the schema |
| Combined filters surprise users | Define AND explicitly; test each filter alone and in combination; omitted param means “no constraint” |
| Service/storage mix | Keep overdue, change-date, and AND filters out of raw persistence; storage remains CRUD (plus at most dumb field equality if a thin service is not added yet) |
| Mini-ADR JSON diagrams vs in-memory Decision | Do not add `tasks.json` or SQLite in this slice; see section 8 |
| Title uniqueness / 50-character limit / required assignee described in the mini-ADR as “existing” rules | Those rules are **not** in the current code or in US-08–US-11 acceptance criteria. Do not add them as part of this extension (see section 8) |
| Filter logic grows large | Optional `date_utils.py` and a thin service function `get_tasks(...)` as in the mini-ADR |

## 7. Suggested Implementation Order

1. **Review** the current modules and existing tests (step 1).
2. **Schemas first:** add `due_date` / `due_date_change_date` / response `overdue` and due-date validation; keep request models from accepting change date or overdue (steps 2–5).
3. **Create path:** persist due date, set change date to null, return computed overdue (steps 6, 10).
4. **Update path:** partial PATCH, invalid date rejection, automatic change-date tracking (steps 7–8).
5. **Overdue helper** with frozen-date tests, including Done and “due today” (step 9).
6. **Wire overdue** into get/list/create/update responses (step 10).
7. **Filters and search:** query params, AND combination, title substring (steps 11–13).
8. **Normalize** records that lack the new fields (step 14).
9. **Tests:** new files plus fixture/regression updates, then full `pytest -v` (steps 15–16).

Do not start frontend work from this document. Do not add JSON-file persistence, a database, auth, or Docker while this order is in progress.

## 8. Open Clarifications

These conflicts are recorded, not silently resolved. Where a later implementation choice is unavoidable, the controlling source is named.

### 8.1 Storage: in-memory vs JSON file

The mini-ADR **Decision** section states that the running app uses in-memory storage, that US-08 to US-11 do not require data to survive a restart, and that this addendum **does not introduce `tasks.json`**.

The same mini-ADR later describes Option A as “FastAPI with Local JSON File Storage,” shows a JSON repository and `tasks.json`, and the Decision Outcome says to continue with “local JSON file storage.” User stories do not mention persistence.

**Actual code** matches the Decision section: `backend/app/storage.py` is in-memory only. README also describes in-memory persistence.

**Controlling for this plan:** keep the current in-memory store. Do not add a database. Do not add `tasks.json` unless a later decision explicitly reverses the mini-ADR Decision paragraph.

### 8.2 Due date required vs legacy tasks without a due date

- US-08 AC4 and US-10 AC3: due date is required; a task with no due date is not possible.
- Mini-ADR overdue exceptions and risks: older stored tasks may lack `due_date`; those tasks are not overdue; missing due dates should be handled safely on read.

**Controlling for create/update:** due date is required on create (US-08 AC4; mini-ADR validation). **Controlling for reads of old records:** tolerate missing `due_date` and treat as not overdue (mini-ADR), without allowing new creates to omit it.

### 8.3 US-10 AC4 “overdue flag is no longer returned” vs always-present boolean

US-10 AC4: when status changes to Done, “the overdue flag is no longer returned.”

Mini-ADR response example always includes `"overdue": false`. AC2 says Done is never marked overdue.

**Not resolved.** Implementation should not omit the field from `TaskResponse` unless product owners confirm omission. This plan treats the mini-ADR schema (always include `overdue: bool`, false for Done) as the API shape, because FastAPI `response_model=TaskResponse` needs a stable field. Confirm whether AC4 means “flag is false” or “field is absent.”

### 8.4 Field name `due_date_change_date` vs `due_date_changed_date`

The mini-ADR risks table mentions both spellings. The data model, JSON examples, validation, and service text use `due_date_change_date`. User stories use the phrase “due date change date” without a snake_case name.

**Controlling:** `due_date_change_date`.

### 8.5 Mini-ADR “existing validation” vs current code and user stories

The mini-ADR says existing rules remain unchanged, including title max **50** characters, **unique** title, and **required** assignee.

Current code (`models.py`): title max **200**, title not unique, assignee **optional**. US-01 requires title; it does not state uniqueness, 50-character max, or required assignee. US-08 says description remains optional and due date is required.

**Controlling for this extension:** do not add title uniqueness, do not change the 200-character limit, and do not newly require assignee, unless a separate decision updates US-01. Only add due-date rules on top of the validation that actually exists.

### 8.6 US-09 404 wording

US-09 AC5 expects a `"Task not found"` error. Current API uses `Task with id {task_id} not found` for get/patch/delete. This plan keeps the existing detail string for consistency with US-05/US-07 behavior unless the exact US-09 text is required.

### 8.7 Server date: local vs UTC

US-09/US-10 and the mini-ADR say “current system date” / “backend/server system date.” The app already stamps `created_at`/`updated_at` in **UTC**. Whether `current_server_date()` is `date.today()` (local) or `datetime.now(timezone.utc).date()` is not specified. Pick one helper and use it in overdue and `due_date_change_date` so both cannot drift apart. Tests must freeze that helper.

### 8.8 Filter match rules not fully specified

US-11 requires filters for due date, overdue, assignee, and title search with AND. It specifies partial case-insensitive match **only** for title. This plan assumes **exact** match for `due_date`, `status`, `priority`, and `assignee` (same pattern as today’s status/priority filters). Date ranges, multiple assignees, or comma-separated values are not specified and are out of scope.

### 8.9 US-06 workflow (out of scope for this extension, still a source conflict)

User stories already record that “forward-only” wording conflicts with allowed **Done → InProgress**, and that numbered US-06 criteria omit ToDo → Done (disallowed) and Done → InProgress (allowed) which appear in the notes. Current `business_rules.py` implements the notes. This plan does not change transitions.

### 8.10 US-01 create fields vs US-08 required due date

US-01 lists create fields without due date. US-08 extends create and requires due date. User stories treat US-08 as an extension of create, not a rewrite of US-01 wording. This plan follows US-08 for create validation.

### 8.11 Hypothetical ADR folder tree vs this repository

Mini-ADR recommended `api/tasks.py`, `schemas/task.py`, `services/task_service.py`, and `json_task_repository.py`. Those files do not exist. This plan uses `main.py`, `models.py`, `business_rules.py`, and `storage.py`, and only optionally adds a thin service or `utils/date_utils.py`.
