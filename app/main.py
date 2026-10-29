from fastapi import FastAPI

from .routers import post, user

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)