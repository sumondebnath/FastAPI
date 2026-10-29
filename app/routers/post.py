from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session

from app import models, schemas, utils, database


router = APIRouter()


@router.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts
    # return {"Posts": posts, "status_code": status.HTTP_200_OK}

@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # return {"Post": post, "status_code": status.HTTP_200_OK}
    return post


@router.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"Post": new_post, "status_code": status.HTTP_201_CREATED}
    return new_post


@router.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id:int, updated_post:schemas.PostCreate, db:Session = Depends(database.get_db)):
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


@router.delete("/posts/{post_id}")
def delete_post(post_id:int, db:Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    deleted_post = post.first()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)