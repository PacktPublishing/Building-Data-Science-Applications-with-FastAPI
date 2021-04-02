from fastapi import FastAPI

from chapter3_project.routers.posts import router as posts_router
from chapter3_project.routers.users import router as users_router

app = FastAPI()

app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(users_router, prefix="/users", tags=["users"])
