from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.models as models
from app.schemas import Post 
from app.database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # return posts
    return {"Posts": posts, "status_code": status.HTTP_200_OK}

@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"Post": post, "status_code": status.HTTP_200_OK}


@app.post("/create/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, author=post.author)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Post": new_post, "status_code": status.HTTP_201_CREATED}


@app.put("/update/posts/{post_id}")
def update_post(post_id:int, updated_post:Post, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    new_post = post.first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # post.title = updated_post.title
    # post.content = updated_post.content
    # post.author = updated_post.author

    updated_data = updated_post.model_dump()
    post.update(updated_data, synchronize_session=False)

    db.commit()
    db.refresh(new_post)
    return {"Post": new_post, "status_code": status.HTTP_200_OK}

    