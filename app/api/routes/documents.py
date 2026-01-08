from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.crud.document import create_document

router = APIRouter()

@router.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document_endpoint(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    return create_document(db, document)
