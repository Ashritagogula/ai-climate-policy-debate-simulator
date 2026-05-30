from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_debate():
    response = client.post(
        "/debate/start",
        json={
            "topic": "Climate Change",
            "rounds": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["messages"]) == 6