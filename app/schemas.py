from pydantic import BaseModel, Field, ConfigDict


class Post(BaseModel):
    title : str = Field(..., max_length=100)
    content : str = Field(..., max_length=1000)
    author : str = Field(..., max_length=100)


# class PostCreate(BaseModel):
#     pass

# class PostResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id = int
#     created_at = str


