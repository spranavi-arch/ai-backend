from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_create_document():
    email = f"doc_owner_{uuid.uuid4()}@example.com"

    user_response = client.post(
        "/users",
        json={
            "name": "Doc Owner",
            "email": email
        }
    )
    user_id = user_response.json()["id"]

    response = client.post(
        "/documents", json={
            "title": "Test Document",
            "content": "Test",
            "owner_id": user_id
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Document"
    assert data["owner_id"] == user_id


def test_get_documents_by_user():
    # Create unique user
    email = f"user_{uuid.uuid4()}@example.com"

    user_response = client.post(
        "/users",
        json={
            "name": "Bob",
            "email": email
        }
    )
    user_id = user_response.json()["id"]

    # Create documents for that user
    client.post(
        "/documents",
        json={
            "title": "Doc 1",
            "content": "Content 1",
            "owner_id": user_id
        }
    )

    client.post(
        "/documents",
        json={
            "title": "Doc 2",
            "content": "Content 2",
            "owner_id": user_id
        }
    )

    # Fetch documents
    response = client.get(f"/users/{user_id}/documents")

    assert response.status_code == 200
    documents = response.json()

    assert len(documents) == 2
    assert all(doc["owner_id"] == user_id for doc in documents)


def test_create_document_validation_error():
    response = client.post(
        "/documents",
        json={
            "content": "Missing title",
            "owner_id": "invalid-id"
        }
    )

    assert response.status_code == 422
