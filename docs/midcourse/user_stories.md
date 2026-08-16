# Task Tracker Extented Features - User Stories

## 1. Purpose

This document records the approved user stories for the Task Tracker learning application. It is the source of truth for existing functional scope and the due-date / search extension. The application is a learning project (Python/FastAPI backend, Pydantic validation, and a simple HTML/CSS/JavaScript frontend) and is not intended to be production software.

## 2. Scope

The Task Tracker maintains **one shared task list** for a solo developer or small team.

**Existing scope** covers:

- Creating tasks
- Viewing all tasks
- Filtering tasks by status and by priority
- Updating task details
- Updating task status according to the workflow in US-06
- Deleting tasks

**Extension scope** covers:

- Required due date on create
- Due date change date (empty until the due date is modified after creation)
- Overdue task detection
- Ability to update the due date
- Automatic update of the due date change date when the due date changes
- Search and filtering by due date, overdue flag, assignee, and task name (in addition to existing status and priority filters)

## 3. Out of Scope

The following are explicitly out of scope:

- Authentication
- User accounts
- Multi-tenancy
- Per-user task lists
- Real-time updates
- Mobile app
- Notifications
- Microservices
- Docker
- Cloud deployment
- Production database setup

## 4. User Stories

### Extension Scope


| ID    | Story                                                                                                                                       | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Notes / Assumptions                                                                                                                                             |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| US-08 | As a team member, I want to assign a due date to a task so that I know when the task is expected to be completed.                           | 1. A due date can be provided when creating a task. 2. The due date is stored and displayed when the task is viewed. 3. The due date must be a valid calendar date; an invalid date format is rejected with a validation error. 4. If no due date is provided, the task is not created and an error message indicate that a due date is required. 5. The due date change date is empty when the due date has never been modified after task creation.                                                                                   | - Description remains optional. Due date is required. - Creating a task with an initial due date does not count as a due date change.                           |
| US-09 | As a team member, I want to update a task's due date so that I can keep the schedule accurate when priorities or timelines change.          | 1. A task's due date can be updated after the task has been created. 2. When the due date is successfully changed, the due date change date is automatically set to the current system date. 3. Updating other task attributes without changing the due date does not modify the due date change date. 4. An invalid due date value is rejected with a validation error and neither the due date nor the due date change date is updated. 5. Attempting to update the due date of a non-existent task returns a "Task not found" error. | - The due date change date is system-generated and cannot be manually supplied by the user. - "Current system date" refers to the server date.                  |
| US-10 | As a team member, I want the system to identify overdue tasks so that I can quickly focus on work requiring immediate attention.            | 1. A task is considered overdue when the current system date is later than its due date and its status is ToDo or InProgress. 2. A task with status Done is never marked as overdue, regardless of its due date. 3. A task with no due date is not possible as due date is required. 4. When the status changes to Done, the overdue flag is automatically set-off. 5. If the due date is today, the task is not considered overdue until the due date has passed according to the application's date comparison rule.                  | - The overdue flag is derived from existing data and is not stored separately. - Date comparison uses the server's system date.                                 |
| US-11 | As a team member, I want to search and filter tasks using task details and due-date information so that I can quickly locate relevant work. | 1. Tasks can be additionally be filtered by due date. 2. Tasks can be additionally be filtered by overdue status (overdue or not overdue). 3. Tasks can be additionally be filtered by assignee. 4. Tasks can be searched by task title (task name). 5. If no tasks match the selected search or filter criteria, the system displays an empty result and an appropriate message.                                                                                                                                                       | - Multiple filters may be applied together using logical AND. - Task name search is assumed to be a partial, case-insensitive match unless otherwise specified. |




## 5. General Assumptions

The following assumptions appear explicitly in the provided stories or project context:

- The application is a learning project and is not intended to be production software.
- There is one shared task list for a solo developer or small team.
- Authentication and user-specific task lists are out of scope.
- Title is required.
- Description remains optional.
- Status values are limited to ToDo, InProgress, and Done.
- Priority values are limited to Low, Medium, and High.
- Deletion permanently removes the task; no recovery or recycle bin is required.
- Due date is required.
- Creating a task with an initial due date does not count as a due date change.
- The due date change date is system-generated and cannot be manually supplied by the user.
- "Current system date" refers to the server date.
- The overdue flag is derived from existing data and is not stored separately.
- Date comparison uses the server's system date.
- Multiple filters may be applied together using logical AND.
- Task name search is assumed to be a partial, case-insensitive match unless otherwise specified.



## 6. Notes for Implementation

These notes are derived only from the provided acceptance criteria:

- Create a task only when required fields are present. Reject a missing or empty title with a validation error (US-01). After the extension, also reject a missing due date and reject an invalid due date format (US-08).
- Newly created tasks must appear in the shared list immediately (US-01). Display title, status, priority, and assignee for each task; show an empty-state message when no tasks exist (US-02). After the extension, also store and display the due date (US-08).
- Status and priority filters each show only matching tasks, restore the full list when cleared, and show an appropriate message when nothing matches (US-03, US-04).
- Updates may change title, description, priority, and assignee. Status changes must be validated against US-06 before save. Updating a non-existent task returns an error and saves nothing (US-05).
- Allowed status transitions in the US-06 notes: ToDo → InProgress, InProgress → Done, Done → InProgress. Disallowed: InProgress → ToDo, Done → ToDo, ToDo → Done. Invalid transitions return a validation error; a rejected Done → ToDo attempt leaves the task Done (US-06).
- Delete removes the task from the shared list. Deleting a non-existent task returns an appropriate error (US-07).
- On create, the due date change date stays empty; setting the initial due date is not a due date change (US-08).
- On a successful due date update, set the due date change date to the server's current date. Do not change that field when other attributes are updated. Reject an invalid due date without changing either date field. Updating a non-existent task's due date returns `"Task not found"` (US-09).
- Treat a task as overdue only when the server date is later than the due date and status is ToDo or InProgress. Done is never overdue. A due date of today is not overdue until that date has passed. After status changes to Done, do not return the overdue flag. Do not persist a separate overdue flag (US-10).
- Additional filters: due date, overdue / not overdue, and assignee. Search by task title. Combine filters with AND. Show an empty result and an appropriate message when nothing matches (US-11).



## Open Clarification

The following inconsistencies appear in the provided source material. They are recorded here and are not resolved in this document.

1. **Status workflow vs. "forward-only".** The existing-scope context describes status updates as a forward-only workflow. US-06 notes explicitly allow **Done → InProgress**, which is not a forward-only transition. US-06 acceptance criteria do not mention Done → InProgress; they only require that Done cannot be changed to ToDo.
2. **US-06 acceptance criteria vs. US-06 notes.** The numbered acceptance criteria allow ToDo → InProgress, allow InProgress → Done, reject InProgress → ToDo, and reject Done → ToDo. The notes additionally list **ToDo → Done** as disallowed and **Done → InProgress** as allowed. Those two transitions are not stated in the numbered acceptance criteria.
3. **US-01 required fields vs. US-08 required due date.** US-01 describes create with title, description, status, priority, and assignee, and names title as required. US-08 states that due date is required and that a task must not be created without one. This document treats US-08 as extension of create; it does not change US-01's wording.
4. **US-06 story wording.** The US-06 story text is incomplete ("if has progressed or was completed") and has no "so that" clause. The wording is preserved as provided.

