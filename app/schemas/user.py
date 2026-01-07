from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(UserCreate):
    id: str

    class Config:
        from_attributes = True
