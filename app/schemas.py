from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime


class PostCreate(BaseModel):
    title : str
    content : str
    author : str


class PostResponse(PostCreate):
    id : int

    class Config:
        orm_model = True


class UserCreate(BaseModel):
    name : str
    email : str
    password : str


class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    created_at : datetime

    class Config:
        orm_model = True


class LoginRequest(BaseModel):
    email : EmailStr
    password : str