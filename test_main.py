from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "To-Do List" in response.text

def test_add_task():
    response = client.post("/add", data={"task": "Test Task"})
    assert response.status_code == 303  # Redirect
    home = client.get("/")
    assert "Test Task" in home.text

def test_toggle_task():
    client.post("/add", data={"task": "Toggle Task"})
    home_before = client.get("/")
    # find the index of last task
    task_id = len(home_before.text.split("✔️")) - 2
    response = client.get(f"/toggle/{task_id}")
    assert response.status_code == 303

def test_delete_task():
    client.post("/add", data={"task": "Delete Task"})
    home_before = client.get("/")
    task_id = len(home_before.text.split("🗑️")) - 2
    response = client.get(f"/delete/{task_id}")
    assert response.status_code == 303

def test_clear_tasks():
    client.post("/add", data={"task": "Clear Me"})
    response = client.post("/clear")
    assert response.status_code == 303