from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

import app.models as models
from app.schemas import PostCreate, PostResponse, UserCreate, UserResponse
from app.database import engine, get_db
from app.utils import hash_password

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "This is the root!"}


@app.get("/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    # return {"Posts": posts, "status_code": status.HTTP_200_OK}

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # return {"Post": post, "status_code": status.HTTP_200_OK}
    return post


@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"Post": new_post, "status_code": status.HTTP_201_CREATED}
    return new_post


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id:int, updated_post:PostCreate, db:Session = Depends(get_db)):
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
    # return {"Post": new_post, "status_code": status.HTTP_200_OK}
    return new_post


@app.delete("/posts/{post_id}")
def delete_post(post_id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    deleted_post = post.first()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user.password = hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user