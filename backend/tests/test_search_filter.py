from datetime import date

DEFAULT_DUE_DATE = "2026-12-31"
FROZEN_TODAY = date(2026, 8, 14)


def _freeze_today(monkeypatch):
    monkeypatch.setattr("app.business_rules.server_today", lambda: FROZEN_TODAY)
    monkeypatch.setattr("app.storage.server_today", lambda: FROZEN_TODAY)


def _create(client, **fields):
    payload = {"due_date": DEFAULT_DUE_DATE, **fields}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201, response.json()
    return response.json()


def test_filter_by_due_date_returns_only_matches(client):
    _create(client, title="aug", due_date="2026-08-20")
    _create(client, title="sep", due_date="2026-09-01")

    response = client.get("/tasks", params={"due_date": "2026-08-20"})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["aug"]


def test_filter_by_overdue_true_returns_only_overdue(client, monkeypatch):
    _freeze_today(monkeypatch)
    _create(client, title="late", due_date="2026-08-01")
    _create(client, title="on-time", due_date="2026-08-20")

    response = client.get("/tasks", params={"overdue": True})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["late"]
    assert all(task["overdue"] is True for task in body)


def test_filter_by_overdue_false_excludes_overdue(client, monkeypatch):
    _freeze_today(monkeypatch)
    _create(client, title="late", due_date="2026-08-01")
    _create(client, title="on-time", due_date="2026-08-20")

    response = client.get("/tasks", params={"overdue": False})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["on-time"]


def test_filter_by_assignee_exact_match(client):
    _create(client, title="alice-task", assignee="alice")
    _create(client, title="bob-task", assignee="bob")

    response = client.get("/tasks", params={"assignee": "alice"})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["alice-task"]


def test_search_by_title_partial_case_insensitive(client):
    _create(client, title="Prepare Sprint Review")
    _create(client, title="Write docs")

    response = client.get("/tasks", params={"title": "sprint"})
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["Prepare Sprint Review"]


def test_combined_filters_use_logical_and(client, monkeypatch):
    _freeze_today(monkeypatch)
    _create(
        client,
        title="Alice overdue high",
        assignee="alice",
        priority="High",
        status="ToDo",
        due_date="2026-08-01",
    )
    _create(
        client,
        title="Alice future high",
        assignee="alice",
        priority="High",
        status="ToDo",
        due_date="2026-08-20",
    )
    _create(
        client,
        title="Bob overdue high",
        assignee="bob",
        priority="High",
        status="ToDo",
        due_date="2026-08-01",
    )

    response = client.get(
        "/tasks",
        params={
            "assignee": "alice",
            "priority": "High",
            "overdue": True,
            "title": "overdue",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert [task["title"] for task in body] == ["Alice overdue high"]


def test_filters_no_match_returns_empty_list(client):
    _create(client, title="something", assignee="alice")
    response = client.get("/tasks", params={"assignee": "nobody", "title": "missing"})
    assert response.status_code == 200
    assert response.json() == []
