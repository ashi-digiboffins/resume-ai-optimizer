from fastapi.testclient import TestClient

from app.main import app


def test_health():
    resp = TestClient(app).get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_extract_endpoint():
    client = TestClient(app)
    resp = client.post(
        "/api/extract", params={"job_description": "Backend engineer, 5 years Go and AWS."}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "go" in body["skills"]
    assert body["years_experience"] == 5
