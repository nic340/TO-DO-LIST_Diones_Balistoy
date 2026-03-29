from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "🌸 Task Dashboard" in response.text

def test_add_task():
    response = client.post("/add", data={"task": "Test Task"}, allow_redirects=False)
    assert response.status_code == 303  # Redirect after adding

def test_toggle_task():
    # Add task first
    client.post("/add", data={"task": "Toggle Task"}, allow_redirects=False)
    # Toggle the last task
    task_id = len(client.get("/").text.split("✔️")) - 2
    response = client.get(f"/toggle/{task_id}", allow_redirects=False)
    assert response.status_code == 303

def test_delete_task():
    # Add task first
    client.post("/add", data={"task": "Delete Task"}, allow_redirects=False)
    # Delete the last task
    task_id = len(client.get("/").text.split("🗑️")) - 2
    response = client.get(f"/delete/{task_id}", allow_redirects=False)
    assert response.status_code == 303

def test_clear_tasks():
    # Add task first
    client.post("/add", data={"task": "Clear Me"}, allow_redirects=False)
    response = client.post("/clear", allow_redirects=False)
    assert response.status_code == 303