from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List


from app.models.document import Document

from app.core.database import get_db
from app.crud.document import get_all_documents
from app.schemas.document import DocumentListResponse, DocumentDetailResponse

router = APIRouter(
    prefix="/documents/all",
    tags=["Documents"]
)

@router.get(
    "",
    response_model=List[DocumentListResponse]
)
def list_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)

@router.get(
    "/{document_id}",
    response_model=DocumentDetailResponse
)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc
