import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def _reset_storage():
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


DEFAULT_DUE_DATE = "2026-12-31"


@pytest.fixture
def created_task(client):
    response = client.post(
        "/tasks",
        json={"title": "fixture task", "due_date": DEFAULT_DUE_DATE},
    )
    assert response.status_code == 201
    return response.json()
