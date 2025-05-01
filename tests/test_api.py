from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_greet_endpoint():
    payload = {"request_id": 1, "name": "Alice"}
    response = client.post("/greet", json=payload)
    assert response.status_code == 200
    assert response.json() == {"request_id": 1, "message": "Hello, Alice!"}
