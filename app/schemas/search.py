from pydantic import BaseModel

class IndexDocumentRequest(BaseModel):
    document_id: int


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
