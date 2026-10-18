from pydantic import BaseModel, Field, ConfigDict


class PostCreate(BaseModel):
    title : str
    content : str
    author : str


# class PostCreate(BaseModel):
#     pass

class PostResponse(PostCreate):
    id : int

    class Config:
        orm_model = True


