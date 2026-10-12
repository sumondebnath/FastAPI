from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     image = Column(String, nullable=True)
#     posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False) 
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = Column(String, nullable=False)