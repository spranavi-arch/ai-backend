from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.document import DocumentCreate, DocumentResponse
from app.crud.document import create_document, get_documents_by_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document_endpoint(doc: DocumentCreate, db: Session = Depends(get_db)):
    return create_document(db, doc)

@router.get("/users/{user_id}/documents", response_model=list[DocumentResponse])
def get_user_documents(user_id: str, db: Session = Depends(get_db)):
    return get_documents_by_user(db, user_id)
