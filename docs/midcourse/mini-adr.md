# ADR-001 Addendum: Due Date, Overdue Logic, and Advanced Filtering


|                     |                                   |
| ------------------- | --------------------------------- |
| **Status**          | Proposed                          |
| **Date**            | August 13, 2026                   |
| **Decision Owners** | Task Tracker project team         |
| **Project**         | Task Tracker learning application |


## Context

The existing Task Tracker application uses a Python/FastAPI backend, Pydantic validation, a simple HTML/CSS/JavaScript frontend, and in-memory storage. Tasks are kept in process memory for the lifetime of the running application and are not persisted to a file. Data does not survive a process restart.

The current architecture already separates the application into:

- FastAPI routes
- Pydantic schemas
- Task service
- In-memory task store
- Simple frontend

The application is now being extended to support the following additional requirements:

- Each task must have a due date.
- Each task has a due date change date.
- A task is overdue when its due date has passed and its status is still ToDo or InProgress.
- A task due date can be changed.
- When the due date is changed, the due date change date is automatically updated using the current server date.
- Tasks can be filtered and searched by:
  - due date
  - overdue flag
  - status
  - priority
  - assignee
  - task name

The following remain explicitly out of scope:

- Authentication
- User accounts
- Multi-tenancy or per-user task lists
- Real-time updates
- Mobile app
- Notifications
- Microservices
- Docker
- Cloud deployment
- Production database setup

The target user remains a solo developer or small team managing work in one shared task list.

## Decision

The existing architecture remains suitable for the new requirements.

An inconsistency was inspected between this addendum’s original storage assumption and the running application. The draft treated **Option A** as FastAPI with persistent local JSON file storage (`tasks.json`), including a JSON repository that reads and writes that file across restarts. The implemented Task Tracker keeps tasks in an in-memory store for the lifetime of the process only. The approved user stories (US-08 to US-11) require due date, due date change date, overdue detection, and filtering on the shared task list; they do not require data to survive a restart. This addendum resolves the inconsistency by keeping in-memory storage and by not introducing `tasks.json` for the due-date extension.

The recommended decision is to keep **Option A: FastAPI with JSON file storage** as the selected architecture.

The new requirements do not require a major architecture change. They require controlled extensions to the existing:

- task data model
- Pydantic validation schemas
- service-layer business rules
- in-memory task store
- filtering and search logic
- frontend task display and filter controls
- automated tests

The architecture should continue to follow the same layered structure:

```text
Browser
 ↓
Uvicorn
 ↓
FastAPI routes
 ↓
Pydantic validation
 ↓
Task service
 ↓
In-memory task store
```

The overdue flag should not be stored as a permanent field on the task record.

It should be calculated dynamically by the service layer based on:

```text
current server date > due_date
AND status is ToDo or InProgress
```

The due date change date should be stored on the in-memory task record because it records a historical event: the last date on which the task due date was changed. Data in the in-memory store does not survive a process restart.

## Rationale



### Existing architecture fit

The current architecture fits the new requirements because the extension introduces business rules and additional fields, not a new architectural need.

The new functionality can be handled through the existing layers:


| Requirement                          | Existing Layer That Can Support It             | Required Change                            |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------ |
| Add due date to task                 | Pydantic schema, domain model, JSON repository | Add `due_date` field                       |
| Validate due date                    | Pydantic schema                                | Require valid date format                  |
| Reject missing due date on create    | Pydantic schema                                | Make `due_date` required in create request |
| Track due date change date           | Service layer                                  | Update automatically when due date changes |
| Detect overdue tasks                 | Service layer                                  | Compute derived overdue flag               |
| Filter by due date                   | Service layer / repository interface           | Add filter parameter                       |
| Filter by overdue flag               | Service layer                                  | Compute overdue before filtering           |
| Search by task name                  | Service layer                                  | Add partial, case-insensitive title search |
| Filter by status, priority, assignee | Existing filtering logic                       | Extend combined filtering                  |


No new infrastructure is required.

### Simplicity

Keeping JSON file storage preserves the learning-project simplicity. The application can still be run locally with minimal setup and without database initialization.

### Testability

The new rules are testable with pytest and FastAPI TestClient.

Tests should cover:

- creating a task with a valid due date
- rejecting a task without a due date
- rejecting invalid due date formats
- changing a due date
- automatically updating the due date change date
- ensuring due date change date does not change when unrelated fields are updated
- calculating overdue tasks correctly
- ensuring Done tasks are not overdue
- filtering by due date
- filtering by overdue flag
- filtering by status, priority, and assignee
- searching by task name
- combining filters using logical AND



### Local run/deploy ability

The application remains easy to run locally.

No Docker, cloud deployment, production database, or external service is required.

### Familiarity

The stack remains consistent with the current learning objective:

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON file storage
- HTML/CSS/JavaScript frontend

This allows the developer to focus on REST API design, validation, business rules, filtering, and testing.

## Architecture



### Option A: FastAPI with Local JSON File Storage

This is the recommended option.

#### Overview

Option A keeps the existing architecture and extends it with due-date-related fields and business rules.

```text
Frontend
 ↓
FastAPI Routes
 ↓
Pydantic Schemas
 ↓
Task Service
 ↓
JSON Repository
 ↓
tasks.json
```



#### Updated data model

The task model should be extended as follows:


| Field                  | Type           | Required | Stored? | Notes                                  |
| ---------------------- | -------------- | -------- | ------- | -------------------------------------- |
| `id`                   | string or UUID | Yes      | Yes     | Generated by the system                |
| `title`                | string         | Yes      | Yes     | Required, unique, max 50 characters    |
| `description`          | string or null | No       | Yes     | Optional                               |
| `status`               | enum           | Yes      | Yes     | ToDo, InProgress, Done                 |
| `priority`             | enum           | Yes      | Yes     | Low, Medium, High                      |
| `assignee`             | string         | Yes      | Yes     | Required                               |
| `due_date`             | date           | Yes      | Yes     | Required on create                     |
| `due_date_change_date` | date or null   | No       | Yes     | System-generated when due date changes |
| `overdue`              | boolean        | No       | No      | Computed dynamically in response       |




#### Suggested JSON example

```json
{
  "id": "9d0d7e5a-9e9f-4f5c-b9c2-4a9c5c80b111",
  "title": "Prepare sprint review",
  "description": "Prepare notes and demo points",
  "status": "InProgress",
  "priority": "High",
  "assignee": "Team Member",
  "due_date": "2026-08-20",
  "due_date_change_date": null
}
```

The API response may include the computed field:

```json
{
  "id": "9d0d7e5a-9e9f-4f5c-b9c2-4a9c5c80b111",
  "title": "Prepare sprint review",
  "description": "Prepare notes and demo points",
  "status": "InProgress",
  "priority": "High",
  "assignee": "Team Member",
  "due_date": "2026-08-20",
  "due_date_change_date": null,
  "overdue": false
}
```



#### Validation changes

Pydantic should validate:

- `due_date` is required when creating a task.
- `due_date` must be a valid date.
- Invalid date formats are rejected.
- `due_date_change_date` cannot be supplied by the client.
- `overdue` cannot be supplied by the client.
- Existing validation rules remain unchanged:
  - title required
  - title not whitespace-only
  - title maximum 50 characters
  - title unique
  - assignee required
  - valid status
  - valid priority



#### Service-layer changes

The task service should be extended to:

- create tasks with a required due date
- store the due date in `tasks.json`
- set `due_date_change_date` to `null` when a task is first created
- update `due_date_change_date` only when the due date changes
- avoid changing `due_date_change_date` when other fields are updated
- calculate overdue dynamically when tasks are returned
- ensure Done tasks are never returned as overdue
- support combined filtering using logical AND
- support partial, case-insensitive task title search



#### Overdue rule

A task is overdue when:

```text
task.due_date < current_server_date
AND task.status IN ["ToDo", "InProgress"]
```

A task is not overdue when:

- the due date is today
- the due date is in the future
- the task status is Done
- the task has no due date in legacy data

Although new tasks require a due date, the system may still need to handle older stored tasks that do not yet have a due date.

#### Filtering and search logic

Filtering can remain in the service layer after loading tasks from the JSON file.

Suggested service method:

```python
get_tasks(
    status=None,
    priority=None,
    assignee=None,
    due_date=None,
    overdue=None,
    title=None
)
```

Suggested processing order:

1. Load tasks from `tasks.json`.
2. Normalize stored task data.
3. Compute overdue for each task.
4. Apply all supplied filters using logical AND.
5. Apply partial, case-insensitive title search.
6. Return matching tasks.



#### Updated folder structure

The existing folder structure can remain unchanged.

Recommended additions are limited to tests and, optionally, a small utility file for date handling.

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── tasks.py
│   ├── schemas/
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   ├── storage/
│   │   └── json_task_repository.py
│   └── utils/
│       └── date_utils.py        # optional
│
│
├── tests/
│   ├── test_due_date.py
│   ├── test_due_date_change.py
│   ├── test_overdue.py
│   └── test_search_filter.py
│
└── requirements.txt
```

The `utils/date_utils.py` file is optional. It may be useful if date comparison logic starts to make the service layer too large.

Possible helper functions:

```python
today()
is_overdue(task)
parse_date(value)
```



#### Frontend changes

The frontend should be extended only enough to support the new requirements.

Required frontend changes:

- Add due date field to task creation form.
- Display task due date in the task list.
- Display due date change date if available.
- Display overdue status.
- Add filters for:
  - due date
  - overdue flag
  - status
  - priority
  - assignee
  - task name

The frontend should not contain the main overdue business rule. It may display the overdue result returned by the API.

### Option B: FastAPI with SQLite and SQLModel

Option B is a lightweight alternative that may improve realism but is not required for the current extension.

#### Overview

Option B keeps FastAPI, Pydantic, and the simple frontend, but replaces JSON file storage with a local SQLite database and SQLModel.

```text
Frontend
 ↓
FastAPI Routes
 ↓
Pydantic Validation
 ↓
Task Service
 ↓
SQLModel Repository
 ↓
SQLite database file
```



#### Why Option B may be considered

Option B may be useful if the learning objective expands to include:

- database tables
- simple SQL-backed persistence
- ORM models
- database sessions
- row-level updates
- database-backed filtering
- more realistic storage patterns



#### Benefits

Option B provides:

- more realistic persistence than JSON files
- better support for filtering queries
- row-level create, update, and delete operations
- stronger consistency than manual JSON file writing
- a good learning bridge toward production-style backend development



#### Costs

Option B introduces additional concepts:

- database setup
- SQLModel models
- sessions
- commits
- migrations or table creation
- repository testing with a temporary test database

These are valuable concepts but may distract from the current learning goal if the main objective remains FastAPI, validation, business rules, and simple local persistence.

#### Option B conclusion

Option B is valid as a future learning step, but it is not necessary for US-08 to US-11.

It should be reconsidered only if the project intentionally moves beyond file-based persistence or if database learning becomes a specific module objective.

## Consequences

### Positive consequences of keeping Option A

- The existing architecture remains stable.
- No major redesign is required.
- No new infrastructure is introduced.
- The learning scope remains focused.
- The project remains easy to run locally.
- The technology stack stays simple and familiar.
- Due date and overdue logic can be added through normal model, schema, service, and test updates.
- The frontend remains simple.
- Filtering can be implemented without introducing database queries.

### Negative consequences of keeping Option A

- Filtering still happens in Python after loading the JSON file.
- The complete JSON file may still be rewritten after updates.
- Date handling must be implemented carefully.
- Existing stored tasks may need to be normalized if they do not already contain `due_date`.
- JSON storage remains less realistic than a database-backed implementation.
- Combined filters may become harder to maintain if many more filters are added later.



### Consequences of Option B

Option B would make filtering and persistence more realistic, but it would also add database and ORM concepts that are not required for the current extension.

For the current project size, Option B may be more than the application needs.

## Risks and Mitigations


| Risk                                                                                    | Mitigation                                                                                                             |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Requirement conflict: US-08 says due date is required, but the notes say it is optional | Treat due date as required because the acceptance criterion explicitly says missing due date must reject task creation |
| Inconsistent field naming such as `due_date_change_date` vs `due_date_changed_date`     | Choose one field name and use it consistently across model, schema, storage, tests, and frontend                       |
| Overdue flag accidentally stored in JSON                                                | Keep overdue as a response-only computed field                                                                         |
| Client sends `due_date_change_date` manually                                            | Reject or ignore client-supplied value; only service layer sets it                                                     |
| Due date change date updates when unrelated fields change                               | Compare old due date with new due date before updating the change date                                                 |
| Done task still appears overdue                                                         | Service layer should always return `overdue = false` when status is Done                                               |
| Current date differs between developer machines                                         | Define date comparison using the backend/server system date                                                            |
| Existing JSON tasks do not contain due date                                             | Add a simple migration/normalization step or handle missing due date safely when reading older data                    |
| Combined filters return unexpected results                                              | Define logical AND as the filtering rule and test combinations                                                         |
| Service layer becomes too large                                                         | Add a small optional `date_utils.py` helper for date comparison and normalization                                      |
| Tests modify real task data                                                             | Use temporary JSON files during tests                                                                                  |




## Alternatives Considered

### Option A: FastAPI with local JSON file storage

Option A keeps the current architecture and extends only the existing layers.

#### Review

Option A is the simplest architecture and remains aligned with the learning project constraints.

It supports the new requirements with minimal changes:

- add due date fields to the model
- update Pydantic validation
- update service-layer business rules
- extend JSON persistence
- add filtering/search logic
- add tests



#### Decision

Option A is recommended.

It is sufficient for the current feature extension and does not introduce unnecessary complexity.

### Option B: FastAPI with SQLite and SQLModel

Option B introduces a lightweight local database.

#### Review

Option B improves realism and provides a better foundation for database-backed filtering. However, it introduces additional learning concepts that are not required to satisfy US-08 to US-11.

#### Decision

Option B is not recommended for this immediate extension.

It remains a valid future option if the project later adds database learning objectives or grows beyond simple local JSON persistence.

## Scope of This Decision

This addendum applies only to the learning-project version of the Task Tracker.

It supports the extension for:

- due date
- due date change date
- overdue calculation
- due date update
- filtering and searching

It does not introduce:

- authentication
- user accounts
- multi-tenancy
- notifications
- real-time updates
- microservices
- Docker
- cloud deployment
- production database setup

This addendum does not replace ADR-001. It extends ADR-001 while preserving the existing architectural direction.

## Decision Outcome

The Task Tracker should continue with FastAPI, Pydantic, Uvicorn, a simple frontend, and local JSON file storage.

The architecture remains suitable for the new requirements.

The implementation should proceed by extending:

- the task data model
- create and update schemas
- service-layer due date logic
- service-layer overdue calculation
- filtering/search logic
- JSON read/write structure
- frontend form and display fields
- automated tests

**Final recommendation:** Adopt Option A for the current extension.

Keep Option B as a future learning path, not as the immediate implementation choice.

## Open Clarification

The following inconsistencies appear in the provided mini-ADR. They are recorded here and are not resolved in this document.

1. **Due date required vs legacy tasks without a due date.** Context and validation state that each task must have a due date, and create must reject a missing due date. The overdue rule and risks also say older stored tasks may have no due date, that such tasks are not overdue, and that missing due dates should be handled safely when reading older data. 
2. `due_date_change_date` **vs** `due_date_changed_date`**.** The risks table names both field spellings. The data model, JSON examples, validation, and service-layer text in this addendum use `due_date_change_date`. This document does not choose a different name.

