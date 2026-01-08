from fastapi import APIRouter
from app.schemas.search import SearchRequest
from app.services.search import semantic_search

router = APIRouter()

@router.post("/search")
def search(payload: SearchRequest):
    document_ids = semantic_search(
        payload.query,
        payload.top_k
    )
    return {"document_ids": document_ids}
