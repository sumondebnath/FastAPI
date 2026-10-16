from pydantic import BaseModel, Field, ConfigDict


class PostCreate(BaseModel):
    title : str = Field(..., max_length=100)
    content : str = Field(..., max_length=1000)
    author : str = Field(..., max_length=100)


# class PostCreate(BaseModel):
#     pass

class PostResponse(PostCreate):
    id : int

    class Config:
        orm_mode = True


