from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
import tempfile

from app.core.database import get_db
from app.services.ocr import extract_text
from app.models.document import Document

router = APIRouter()


@router.post("/documents/upload", status_code=201)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = file.filename.lower()

    if not filename.endswith((".png", ".jpg", ".jpeg", ".pdf")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    tmp_path = None

    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # OCR extraction
        extracted_text = extract_text(tmp_path, filename)

        if not extracted_text or not extracted_text.strip():
            extracted_text = "OCR extraction failed, fallback text"

        document = Document(
            title=file.filename,
            content=extracted_text,
            original_filename=file.filename
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "document_id": document.id,
            "filename": document.original_filename,
            "extracted_text": extracted_text
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
