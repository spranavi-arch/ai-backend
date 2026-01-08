from pydantic import BaseModel

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
