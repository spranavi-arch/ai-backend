from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


def test_upload_image_ocr():
    # Fake image content (simulates scanned image)
    file_content = b"fake image bytes"

    response = client.post(
        "/documents/upload",
        files={
            "file": ("test.png", io.BytesIO(file_content), "image/png")
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert "document_id" in body
    assert "extracted_text" in body
    assert isinstance(body["extracted_text"], str)
    assert len(body["extracted_text"]) > 0


def test_upload_invalid_file_type():
    response = client.post(
        "/documents/upload",
        files={
            "file": ("test.txt", io.BytesIO(b"text"), "text/plain")
        }
    )

    assert response.status_code == 400
