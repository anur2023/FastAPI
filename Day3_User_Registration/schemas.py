from datetime import datetime
from typing import Optional


from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email :EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenDate(BaseModel):
    id:Optional[str] = None