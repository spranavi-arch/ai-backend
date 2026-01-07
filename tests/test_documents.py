from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)


def test_create_document_with_multiple_users():
    u1 = client.post("/users", json={"name": "A", "email": "a@test.com"}).json()
    u2 = client.post("/users", json={"name": "B", "email": "b@test.com"}).json()

    response = client.post(
        "/documents",
        json={
            "title": "Shared Doc",
            "content": "Shared content",
            "user_ids": [u1["id"], u2["id"]]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert len(data["user_ids"]) == 2



def test_get_documents_by_user():
    email = f"user_{uuid.uuid4()}@example.com"

    user = client.post(
        "/users",
        json={"name": "Bob", "email": email}
    ).json()

    user_id = user["id"]

    client.post(
        "/documents",
        json={
            "title": "Doc 1",
            "content": "Content 1",
            "user_ids": [user["id"]]
        }
    )

    client.post(
        "/documents",
        json={
            "title": "Doc 2",
            "content": "Content 2",
            "user_ids": [user["id"]]
        }
    )

    # Fetch documents

    response = client.get(f"/users/{user['id']}/documents")

    assert response.status_code == 200
    documents = response.json()
    assert len(documents) == 2
    assert all(user["id"] in doc["user_ids"] for doc in documents)



    
   


def test_create_document_validation_error():
    response = client.post(
        "/documents",
        json={
            "content": "Missing title",
            "owner_id": "invalid-id"
        }
    )

    assert response.status_code == 422
