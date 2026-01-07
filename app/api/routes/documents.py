from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.document import DocumentCreate
from app.crud.document import create_document

router = APIRouter()

@router.post("/documents", status_code=201)
def create_document_endpoint(
    data: DocumentCreate,
    db: Session = Depends(get_db)
):
    doc = create_document(db, data)
    return {
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "user_ids": [u.id for u in doc.users]
    }
