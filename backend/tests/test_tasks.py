from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_and_read_task():
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    task_id = data["id"]

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert any(t["id"] == task_id for t in tasks)

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_and_delete_task():
    response = client.post("/tasks", json={"title": "Old Title"})
    task_id = response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
