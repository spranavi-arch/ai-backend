from pydantic import BaseModel
from typing import List

class DocumentCreate(BaseModel):
    title: str
    content: str
    user_ids: List[int]



class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    user_ids: List[int]

    class Config:
        from_attributes = True
