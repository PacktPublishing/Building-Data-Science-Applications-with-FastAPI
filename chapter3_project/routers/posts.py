from typing import List

from fastapi import APIRouter, HTTPException, status

from chapter3_project.models.post import Post, PostCreate
from chapter3_project.db import db

router = APIRouter()


@router.get("/")
async def all() -> List[Post]:
    return list(db.posts.values())


@router.get("/{id}")
async def get(id: int) -> Post:
    try:
        return db.posts[id]
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(post_create: PostCreate) -> Post:
    try:
        db.users[post_create.user]
    except KeyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {post_create.user} doesn't exist.",
        )

    new_id = max(db.posts.keys() or (0,)) + 1
    post = Post(id=new_id, **post_create.dict())
    db.posts[new_id] = post
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int) -> None:
    try:
        db.posts.pop(id)
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
