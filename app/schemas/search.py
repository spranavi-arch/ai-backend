from pydantic import BaseModel, Field


class IndexDocumentRequest(BaseModel):
    document_id: int


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    document_id: int
    title: str
    score: float





