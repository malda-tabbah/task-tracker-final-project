from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.business_rules import is_overdue, server_today
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def _with_overdue(task: TaskResponse) -> TaskResponse:
    return task.model_copy(
        update={"overdue": is_overdue(task.due_date, task.status)}
    )


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        due_date_change_date=None,
        overdue=False,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return _with_overdue(task)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
    due_date: Optional[date] = None,
    overdue: Optional[bool] = None,
    title: Optional[str] = None,
) -> list[TaskResponse]:
    tasks = [_with_overdue(task) for task in _tasks.values()]
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if assignee is not None:
        tasks = [task for task in tasks if task.assignee == assignee]
    if due_date is not None:
        tasks = [task for task in tasks if task.due_date == due_date]
    if overdue is not None:
        tasks = [task for task in tasks if task.overdue == overdue]
    if title is not None:
        needle = title.lower()
        tasks = [task for task in tasks if needle in task.title.lower()]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _with_overdue(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    data = existing.model_dump()
    if "due_date" in updates and updates["due_date"] != existing.due_date:
        data["due_date_change_date"] = server_today()
    data.update(updates)
    data["updated_at"] = datetime.now(timezone.utc)
    updated = TaskResponse(**data)
    _tasks[task_id] = updated
    return _with_overdue(updated)


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
