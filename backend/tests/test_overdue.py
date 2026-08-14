from datetime import date

from app.business_rules import is_overdue
from app.models import TaskStatus

FROZEN_TODAY = date(2026, 8, 14)


def _freeze_today(monkeypatch):
    monkeypatch.setattr("app.business_rules.server_today", lambda: FROZEN_TODAY)
    monkeypatch.setattr("app.storage.server_today", lambda: FROZEN_TODAY)


def test_is_overdue_when_due_date_passed_and_todo():
    assert is_overdue(date(2026, 8, 13), TaskStatus.TODO, today=FROZEN_TODAY) is True


def test_is_overdue_when_due_date_passed_and_in_progress():
    assert is_overdue(date(2026, 8, 1), TaskStatus.IN_PROGRESS, today=FROZEN_TODAY) is True


def test_is_overdue_false_when_due_date_is_today():
    assert is_overdue(FROZEN_TODAY, TaskStatus.TODO, today=FROZEN_TODAY) is False


def test_is_overdue_false_when_due_date_is_future():
    assert is_overdue(date(2026, 8, 20), TaskStatus.TODO, today=FROZEN_TODAY) is False


def test_is_overdue_false_when_status_is_done():
    assert is_overdue(date(2026, 8, 1), TaskStatus.DONE, today=FROZEN_TODAY) is False


def test_is_overdue_false_when_due_date_missing():
    assert is_overdue(None, TaskStatus.TODO, today=FROZEN_TODAY) is False


def test_overdue_true_when_due_date_passed_and_todo(client, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.post(
        "/tasks",
        json={"title": "Late todo", "status": "ToDo", "due_date": "2026-08-01"},
    )
    assert response.status_code == 201
    assert response.json()["overdue"] is True


def test_overdue_true_when_due_date_passed_and_in_progress(client, monkeypatch):
    _freeze_today(monkeypatch)
    created = client.post(
        "/tasks",
        json={"title": "Late in progress", "status": "ToDo", "due_date": "2026-08-01"},
    )
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert response.status_code == 200
    assert response.json()["overdue"] is True


def test_overdue_false_when_due_date_is_today(client, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.post(
        "/tasks",
        json={"title": "Due today", "due_date": "2026-08-14"},
    )
    assert response.status_code == 201
    assert response.json()["overdue"] is False


def test_overdue_false_when_due_date_is_future(client, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.post(
        "/tasks",
        json={"title": "Upcoming", "due_date": "2026-08-20"},
    )
    assert response.status_code == 201
    assert response.json()["overdue"] is False


def test_done_task_is_never_overdue(client, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.post(
        "/tasks",
        json={"title": "Finished late", "status": "Done", "due_date": "2026-08-01"},
    )
    assert response.status_code == 201
    assert response.json()["overdue"] is False


def test_overdue_becomes_false_when_status_changes_to_done(client, monkeypatch):
    _freeze_today(monkeypatch)
    created = client.post(
        "/tasks",
        json={"title": "Was late", "status": "ToDo", "due_date": "2026-08-01"},
    )
    task_id = created.json()["id"]
    assert created.json()["overdue"] is True

    in_progress = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert in_progress.json()["overdue"] is True

    done = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert done.status_code == 200
    assert done.json()["overdue"] is False
    assert done.json()["status"] == "Done"
