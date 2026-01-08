from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_create_document():
    user = client.post(
        "/users",
        json={"name": "A", "email": "a@test.com"}
    ).json()

    response = client.post(
        "/documents",
        json={
            "title": "Doc",
            "content": "Text",
            "user_id": user["id"]
        }
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == user["id"]



def test_create_document_validation_error():
    response = client.post(
        "/documents",
        json={
            "content": "Missing title",
            "owner_id": "invalid-id"
        }
    )

    assert response.status_code == 422
