from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_create_user():
    email = f"user_{uuid.uuid4()}@example.com"

    response = client.post(
        "/users",
        json={
            "name": "Alice",
            "email": email
        }
    )

    assert response.status_code == 201



def test_create_user_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Invalid User",
            "email": "not-an-email"
        }
    )

    assert response.status_code == 422

def test_get_documents_by_user():
    user = client.post(
        "/users",
        json={"name": "User", "email": "u@test.com"}
    ).json()

    client.post(
        "/documents",
        json={
            "title": "Doc",
            "content": "Text",
            "user_id": user["id"]
        }
    )

    response = client.get(f"/users/{user['id']}/documents")

    assert response.status_code == 200
    assert len(response.json()) == 1


