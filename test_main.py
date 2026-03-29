from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "🌸 Task Dashboard" in response.text

def test_add_task():
    response = client.request("POST", "/add", data={"task": "Test Task"}, allow_redirects=False)
    assert response.status_code == 303

def test_toggle_task():
    client.request("POST", "/add", data={"task": "Toggle Task"}, allow_redirects=False)
    task_id = len(client.get("/").text.split("✔️")) - 2
    response = client.request("GET", f"/toggle/{task_id}", allow_redirects=False)
    assert response.status_code == 303

def test_delete_task():
    client.request("POST", "/add", data={"task": "Delete Task"}, allow_redirects=False)
    task_id = len(client.get("/").text.split("🗑️")) - 2
    response = client.request("GET", f"/delete/{task_id}", allow_redirects=False)
    assert response.status_code == 303

def test_clear_tasks():
    client.request("POST", "/add", data={"task": "Clear Me"}, allow_redirects=False)
    response = client.request("POST", "/clear", allow_redirects=False)
    assert response.status_code == 303