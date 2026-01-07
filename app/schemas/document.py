from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    content: str
    owner_id: str

class DocumentResponse(DocumentCreate):
    id: str

    class Config:
        from_attributes = True
