from fastapi import FastAPI

from .routers import post, user, auth

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)


app.include_router(post.router, prefix="/api/v1", tags=["Posts"])
app.include_router(user.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])