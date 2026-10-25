from fastapi.testclient import TestClient

from automind_ai.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["indexed_chunks"] >= 1


def test_query_returns_source_passages():
    response = client.post("/query", json={"question": "What does ABS do?", "top_k": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "retrieval_only"
    assert body["result_count"] >= 1
    assert body["results"][0]["source"] == "automotive_systems.md"
    assert "not a generated diagnosis" in body["note"]


def test_query_validates_top_k():
    response = client.post("/query", json={"question": "ABS", "top_k": 0})
    assert response.status_code == 422
