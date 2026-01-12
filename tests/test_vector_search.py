from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index_document():
    # First create a document
    doc = client.post(
        "/documents",
        json={
            "title": "Invoice Doc",
            "content": "This invoice is due on Monday",
            "user_id": 1
        }
    ).json()

    response = client.post(
        "/documents/index",
        json={"document_id": doc["id"]}
    )

    assert response.status_code == 200
    assert response.json()["indexed"] is True


def test_semantic_search_returns_relevant_doc():
    response = client.post(
        "/search",
        json={
            "query": "invoice payment",
            "k": 3
        }
    )

    assert response.status_code == 200

    results = response.json()

    assert isinstance(results, list)
    assert len(results) > 0

    first = results[0]

    assert "document_id" in first
    assert "title" in first
    assert "score" in first
