from pydantic import BaseModel
from typing import Optional

class DocumentCreate(BaseModel):
    title: str
    content: str
    user_id: int


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True

class DocumentListResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    user_id: Optional[int]

    class Config:
        from_attributes = True 

class DocumentDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    original_filename: str | None = None

    class Config:
        from_attributes = True
