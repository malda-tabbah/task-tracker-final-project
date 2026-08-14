from datetime import date
from typing import Optional

from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def server_today() -> date:
    return date.today()


def is_overdue(
    due_date: Optional[date],
    status: TaskStatus,
    today: Optional[date] = None,
) -> bool:
    if due_date is None:
        return False
    if status == TaskStatus.DONE:
        return False
    if today is None:
        today = server_today()
    return today > due_date and status in (TaskStatus.TODO, TaskStatus.IN_PROGRESS)


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    # No-op updates should be allowed. Only real changes need validation.
    if current == new:
        return

    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
