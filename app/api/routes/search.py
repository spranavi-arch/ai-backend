from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.document import Document
from app.schemas.search import SearchRequest, SearchResult
from app.services.search import search_documents

router = APIRouter(tags=["Vector Search"])


@router.post("/search", response_model=list[SearchResult])
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    search_results = search_documents(request.query, request.k)

    if not search_results:
        return []

    doc_ids = [r["document_id"] for r in search_results]

    documents = (
        db.query(Document)
        .filter(Document.id.in_(doc_ids))
        .all()
    )

    doc_map = {doc.id: doc for doc in documents}

    response = []
    for r in search_results:
        doc = doc_map.get(r["document_id"])
        if doc:
            response.append(
                SearchResult(
                    document_id=doc.id,
                    title=doc.title,
                    score=r["score"]
                )
            )

    return response
