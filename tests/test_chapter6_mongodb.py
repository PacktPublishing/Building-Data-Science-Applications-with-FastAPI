import os
from typing import Any, Dict, Optional

import httpx
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import status

from chapter6.mongodb.app import app, get_database
from chapter6.mongodb.models import PostDB


motor_client = AsyncIOMotorClient(
    os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
)
database_test = motor_client["chapter6_mongo_test"]
initial_posts = [
    PostDB(title="Post 1", content="Content 1"),
    PostDB(title="Post 2", content="Content 2"),
    PostDB(title="Post 3", content="Content 3"),
]
existing_id = str(initial_posts[0].id)
not_existing_id = str(ObjectId())
invalid_id = "aaa"


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initialize_database():
    await database_test["posts"].insert_many(
        [post.dict(by_alias=True) for post in initial_posts]
    )

    yield

    await motor_client.drop_database("chapter6_mongo_test")


@pytest.mark.fastapi(
    app=app, dependency_overrides={get_database: lambda: database_test}
)
@pytest.mark.asyncio
class TestChapter6MongoDB:
    @pytest.mark.parametrize(
        "skip,limit,nb_results", [(None, None, 3), (0, 1, 1), (10, 1, 0)]
    )
    async def test_list_posts(
        self,
        client: httpx.AsyncClient,
        skip: Optional[int],
        limit: Optional[int],
        nb_results: int,
    ):
        params = {}
        if skip:
            params["skip"] = skip
        if limit:
            params["limit"] = limit
        response = await client.get("/posts", params=params)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) == nb_results
        for post in json:
            assert "_id" in post

    @pytest.mark.parametrize(
        "id,status_code",
        [
            (existing_id, status.HTTP_200_OK),
            (not_existing_id, status.HTTP_404_NOT_FOUND),
            (invalid_id, status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_get_post(self, client: httpx.AsyncClient, id: str, status_code: int):
        response = await client.get(f"/posts/{id}")

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            assert json["_id"] == id

    @pytest.mark.parametrize(
        "payload,status_code",
        [
            ({"title": "New post", "content": "New content"}, status.HTTP_201_CREATED),
            ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_create_post(
        self, client: httpx.AsyncClient, payload: Dict[str, Any], status_code: int
    ):
        response = await client.post("/posts", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            json = response.json()
            assert "_id" in json

    @pytest.mark.parametrize(
        "id,payload,status_code",
        [
            (existing_id, {"title": "Post 1 Updated"}, status.HTTP_200_OK),
            (not_existing_id, {"title": "Post 10 Updated"}, status.HTTP_404_NOT_FOUND),
            (invalid_id, {"title": "Post 10 Updated"}, status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_update_post(
        self,
        client: httpx.AsyncClient,
        id: str,
        payload: Dict[str, Any],
        status_code: int,
    ):
        response = await client.patch(f"/posts/{id}", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            for key in payload:
                assert json[key] == payload[key]

    @pytest.mark.parametrize(
        "id,status_code",
        [
            (existing_id, status.HTTP_204_NO_CONTENT),
            (not_existing_id, status.HTTP_404_NOT_FOUND),
            (invalid_id, status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_delete_post(
        self, client: httpx.AsyncClient, id: str, status_code: int
    ):
        response = await client.delete(f"/posts/{id}")

        assert response.status_code == status_code
