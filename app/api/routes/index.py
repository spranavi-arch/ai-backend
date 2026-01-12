from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.schemas.search import IndexDocumentRequest
from app.services.search import index_document_text

router = APIRouter(prefix="/documents", tags=["Vector Search"])


@router.post("/index", status_code=status.HTTP_200_OK)
def index_document_endpoint(
    request: IndexDocumentRequest,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.id == request.document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.content:
        raise HTTPException(status_code=400, detail="Document has no content")

    try:
        index_document_text(document.id, document.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Document indexed successfully"}
