import asyncio
from typing import List

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import status

from chapter6.mongodb.app import app, get_database
from chapter6.mongodb.models import PostDB

motor_client = AsyncIOMotorClient("mongodb://localhost:27017")
database_test = motor_client["chapter9_db_test"]


def get_test_database():
    return database_test


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[get_database] = get_test_database
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initial_posts():
    initial_posts = [
        PostDB(title="Post 1", content="Content 1"),
        PostDB(title="Post 2", content="Content 2"),
        PostDB(title="Post 3", content="Content 3"),
    ]
    await database_test["posts"].insert_many(
        [post.dict(by_alias=True) for post in initial_posts]
    )

    yield initial_posts

    await motor_client.drop_database("chapter9_db_test")


@pytest.mark.asyncio
class TestGetPost:
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/posts/abc")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_existing(
        self, test_client: httpx.AsyncClient, initial_posts: List[PostDB]
    ):
        response = await test_client.get(f"/posts/{initial_posts[0].id}")

        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert json["_id"] == str(initial_posts[0].id)


@pytest.mark.asyncio
class TestCreatePost:
    async def test_invalid_payload(self, test_client: httpx.AsyncClient):
        payload = {"title": "New post"}
        response = await test_client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, test_client: httpx.AsyncClient):
        payload = {"title": "New post", "content": "New post content"}
        response = await test_client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_201_CREATED

        json = response.json()
        post_id = ObjectId(json["_id"])
        post_db = await database_test["posts"].find_one({"_id": post_id})
        assert post_db is not None
