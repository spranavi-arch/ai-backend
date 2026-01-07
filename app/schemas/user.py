from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserWithDocuments(UserResponse):
    document_ids: List[int]
