from fastapi import FastAPI

from .routers import post, user

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)


app.include_router(post.router, prefix="/api/v1", tags=["Posts"])
app.include_router(user.router, prefix="/api/v1", tags=["Users"])