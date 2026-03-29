from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "🌸 Task Dashboard" in response.text

def test_add_task():
    response = client.post("/add", data={"task": "Test Task"})
    # the final response after redirect will be 200
    assert response.status_code == 200
    assert "Test Task" in response.text

def test_toggle_task():
    client.post("/add", data={"task": "Toggle Task"})
    home_before = client.get("/")
    task_id = len(home_before.text.split("✔️")) - 2
    response = client.get(f"/toggle/{task_id}")
    assert response.status_code == 200
    home_after = client.get("/")
    assert "Toggle Task" in home_after.text

def test_delete_task():
    client.post("/add", data={"task": "Delete Task"})
    home_before = client.get("/")
    task_id = len(home_before.text.split("🗑️")) - 2
    response = client.get(f"/delete/{task_id}")
    assert response.status_code == 200

def test_clear_tasks():
    client.post("/add", data={"task": "Clear Me"})
    response = client.post("/clear")
    assert response.status_code == 200