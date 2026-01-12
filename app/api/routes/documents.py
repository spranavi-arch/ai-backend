from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.search import IndexDocumentRequest
from app.services.search import index_document_text
from app.crud.document import create_document
from app.models.document import Document

router = APIRouter()

@router.post(
    "/documents",
    response_model=DocumentResponse,
    status_code=201,
    operation_id="create_document"
)
def create_document_endpoint(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    return create_document(db, document)


@router.post(
    "/documents/index",
    operation_id="index_document"
)
@router.post("/documents/index")
def index_document(payload: IndexDocumentRequest, db: Session = Depends(get_db)):
    document = db.query(Document).get(payload.document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    index_document_text(
        db=db,
        document_id=document.id,
        text=document.content
    )

    return {"indexed":True,"message": "Document indexed with chunking"}
