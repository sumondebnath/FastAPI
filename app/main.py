from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import app.models as models
from app.database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # posts = db.query(models.Post).all()
    # return posts
    return {"message": "This is the posts endpoint."}