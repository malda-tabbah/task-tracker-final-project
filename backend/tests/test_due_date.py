from datetime import date

DEFAULT_DUE_DATE = "2026-12-31"
FROZEN_TODAY = date(2026, 8, 14)


def _freeze_today(monkeypatch):
    monkeypatch.setattr("app.business_rules.server_today", lambda: FROZEN_TODAY)
    monkeypatch.setattr("app.storage.server_today", lambda: FROZEN_TODAY)


def test_create_task_with_valid_due_date_returns_201(client):
    response = client.post(
        "/tasks",
        json={"title": "Has due date", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == DEFAULT_DUE_DATE
    assert body["due_date_change_date"] is None


def test_create_task_missing_due_date_returns_422(client):
    response = client.post("/tasks", json={"title": "No due date"})
    assert response.status_code == 422


def test_create_task_invalid_due_date_format_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Bad date", "due_date": "not-a-date"},
    )
    assert response.status_code == 422


def test_create_task_rejects_client_supplied_due_date_change_date(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Forbidden field",
            "due_date": DEFAULT_DUE_DATE,
            "due_date_change_date": "2026-08-14",
        },
    )
    assert response.status_code == 422


def test_create_task_rejects_client_supplied_overdue(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Forbidden field",
            "due_date": DEFAULT_DUE_DATE,
            "overdue": True,
        },
    )
    assert response.status_code == 422


def test_patch_due_date_sets_change_date_to_server_today(client, created_task, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-09-01"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["due_date"] == "2026-09-01"
    assert body["due_date_change_date"] == "2026-08-14"


def test_patch_same_due_date_does_not_set_change_date(client, created_task, monkeypatch):
    _freeze_today(monkeypatch)
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": created_task["due_date"]},
    )
    assert response.status_code == 200
    assert response.json()["due_date_change_date"] is None


def test_patch_unrelated_field_does_not_change_due_date_change_date(
    client, created_task, monkeypatch
):
    _freeze_today(monkeypatch)
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["due_date"] == created_task["due_date"]
    assert body["due_date_change_date"] is None


def test_patch_invalid_due_date_does_not_change_either_date_field(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "14-08-2026"},
    )
    assert response.status_code == 422

    stored = client.get(f"/tasks/{created_task['id']}")
    assert stored.status_code == 200
    body = stored.json()
    assert body["due_date"] == created_task["due_date"]
    assert body["due_date_change_date"] is None


def test_patch_due_date_missing_task_returns_404(client):
    response = client.patch(
        "/tasks/missing-id",
        json={"due_date": "2026-09-01"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"
