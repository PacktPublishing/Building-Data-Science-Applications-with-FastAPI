from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class Post(BaseModel):
    title: str


app = FastAPI()

# Dummy database
posts = {
    1: Post(title="Hello"),
}


@app.put("/posts/{id}")
async def update_or_create_post(id: int, post: Post, response: Response):
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]
