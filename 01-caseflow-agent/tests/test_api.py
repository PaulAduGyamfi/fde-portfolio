from fastapi.testclient import TestClient
from caseflow.api import app

client = TestClient(app)

HEADERS = {"x-api-key": "definitely-wrong"}
TICKET = {"message_id": "m1", "from_address": "a@b.com",
          "subject": "s", "body": "hello there"}


def test_wrong_api_key_returns_401():
    r = client.post("/handle", headers=HEADERS, json=TICKET)
    assert r.status_code == 401


def test_missing_api_key_is_rejected():
    r = client.post("/handle", json=TICKET)
    assert r.status_code in (401, 422)   # 422 when the header is absent entirely


def test_import_github_requires_a_key():
    r = client.get("/import/github?owner=o&repo=r")
    assert r.status_code in (401, 422)


def test_health_is_open():
    assert client.get("/health").status_code == 200