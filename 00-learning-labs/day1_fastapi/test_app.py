from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ticket_submission():
    payload = {
        "ticket_id": "1234567890",
        "customer_id": "1234567890",
        "subject": "Test Subject",
        "body": "Test Body",
        "channel": "email"
    }
    response = client.post("tickets", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "received"

def test_ticket_submission_rejected():
    payload = {
        "ticket_id": "1234567890",
        "customer_id": "",
        "subject": "Test Subject",
        "body": "Test Body",
        "channel": "email"
    }
    response = client.post("tickets", json=payload)
    assert response.status_code == 422