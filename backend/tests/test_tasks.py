from app.main import app

DEFAULT_DUE_DATE = "2026-12-31"

EXPECTED_TASK_KEYS = {
    "id",
    "title",
    "description",
    "status",
    "priority",
    "assignee",
    "due_date",
    "due_date_change_date",
    "overdue",
    "created_at",
    "updated_at",
}


def test_get_version_returns_200_with_version_string(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": app.version}


def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Buy groceries",
            "description": "Milk and eggs",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alice",
            "due_date": DEFAULT_DUE_DATE,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert set(body.keys()) == EXPECTED_TASK_KEYS
    assert body["title"] == "Buy groceries"
    assert body["description"] == "Milk and eggs"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert body["due_date"] == DEFAULT_DUE_DATE
    assert body["due_date_change_date"] is None
    assert body["overdue"] is False
    assert isinstance(body["id"], str) and body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client):
    response = client.post(
        "/tasks",
        json={"description": "no title", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "   ", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "task", "priority": "Urgent", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "task", "unknown_field": "x", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "a", "status": "ToDo", "due_date": DEFAULT_DUE_DATE})
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "low", "priority": "Low", "due_date": DEFAULT_DUE_DATE})
    client.post("/tasks", json={"title": "high", "priority": "High", "due_date": DEFAULT_DUE_DATE})
    client.post("/tasks", json={"title": "high-2", "priority": "High", "due_date": DEFAULT_DUE_DATE})

    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(task["priority"] == "High" for task in body)
    assert {task["title"] for task in body} == {"high", "high-2"}


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]
    assert response.json()["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id nonexistent-id not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": "updated description"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "updated description"
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]
    assert body["id"] == task_id


def test_patch_null_title_returns_422_and_keeps_original_title(client, created_task):
    task_id = created_task["id"]
    original_title = created_task["title"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": None},
    )
    assert response.status_code == 422

    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == original_title


def test_patch_blank_title_returns_422_and_keeps_original_title(client, created_task):
    task_id = created_task["id"]
    original_title = created_task["title"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "   "},
    )
    assert response.status_code == 422

    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == original_title


def test_patch_empty_title_returns_422_and_keeps_original_title(client, created_task):
    task_id = created_task["id"]
    original_title = created_task["title"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""},
    )
    assert response.status_code == 422

    stored = client.get(f"/tasks/{task_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == original_title


def test_patch_not_found_returns_404(client):
    response = client.patch(
        "/tasks/missing-id",
        json={"title": "new title"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert response.status_code == 422


def test_patch_invalid_transition_done_to_todo_returns_422(client):
    created = client.post(
        "/tasks",
        json={
            "title": "Completed task",
            "status": "Done",
            "due_date": DEFAULT_DUE_DATE,
        },
    )
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"] == (
        "Invalid status transition from Done to ToDo. "
        "Allowed transitions: ['Done->InProgress', 'InProgress->Done', 'ToDo->InProgress']"
    )


def test_patch_same_status_returns_200_and_keeps_status(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ToDo"


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"
