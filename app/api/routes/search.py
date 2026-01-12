from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.search_utils import hydrate_chunks
from app.core.database import get_db
from app.models.document import Document
from app.schemas.search import SearchRequest, SearchResult
from app.services.search import search_chunks

router = APIRouter(tags=["Vector Search"])


#@router.post("/search", response_model=list[SearchResult])

@router.get("/search")
def semantic_search(query: str, k: int = 5, db: Session = Depends(get_db)):
    # 1. FAISS returns chunk_ids
    raw_results = search_chunks(query, k)

    # 2. Hydrate chunks from DB
    chunks = hydrate_chunks(db, raw_results)

    return {
        "query": query,
        "results": chunks
    }

