import os
from typing import Any, Dict, Optional

import httpx
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import status

from chapter6.mongodb_relationship.app import app, get_database
from chapter6.mongodb_relationship.models import CommentDB, PostDB


motor_client = AsyncIOMotorClient(
    os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
)
database_test = motor_client["chapter6_mongo_relationship_test"]
initial_posts = [
    PostDB(
        title="Post 1",
        content="Content 1",
        comments=[
            CommentDB(content="Post 1 Comment 1"),
            CommentDB(content="Post 1 Comment 2"),
            CommentDB(content="Post 1 Comment 3"),
        ],
    ),
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

    await motor_client.drop_database("chapter6_mongo_relationship_test")


@pytest.mark.fastapi(
    app=app, dependency_overrides={get_database: lambda: database_test}
)
@pytest.mark.asyncio
class TestChapter6MongoDBRelationship:
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
        "id,status_code,nb_comments",
        [
            (existing_id, status.HTTP_200_OK, 3),
            (not_existing_id, status.HTTP_404_NOT_FOUND, 0),
            (invalid_id, status.HTTP_404_NOT_FOUND, 0),
        ],
    )
    async def test_get_post(
        self, client: httpx.AsyncClient, id: str, status_code: int, nb_comments: int
    ):
        response = await client.get(f"/posts/{id}")

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            assert json["_id"] == id
            assert len(json["comments"]) == nb_comments

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
            assert json["comments"] == []

    @pytest.mark.parametrize(
        "id,payload,status_code,nb_comments",
        [
            (existing_id, {"title": "Post 1 Updated"}, status.HTTP_200_OK, 3),
            (
                not_existing_id,
                {"title": "Post 10 Updated"},
                status.HTTP_404_NOT_FOUND,
                0,
            ),
            (invalid_id, {"title": "Post 10 Updated"}, status.HTTP_404_NOT_FOUND, 0),
        ],
    )
    async def test_update_post(
        self,
        client: httpx.AsyncClient,
        id: str,
        payload: Dict[str, Any],
        status_code: int,
        nb_comments: int,
    ):
        response = await client.patch(f"/posts/{id}", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            for key in payload:
                assert json[key] == payload[key]
            assert len(json["comments"]) == nb_comments

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

    @pytest.mark.parametrize(
        "post_id,payload,status_code",
        [
            (
                str(initial_posts[1].id),
                {"content": "New comment"},
                status.HTTP_201_CREATED,
            ),
            (not_existing_id, {"content": "New comment"}, status.HTTP_404_NOT_FOUND),
            (str(initial_posts[1].id), {}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_create_comment(
        self,
        client: httpx.AsyncClient,
        post_id: str,
        payload: Dict[str, Any],
        status_code: int,
    ):
        response = await client.post(f"/posts/{post_id}/comments", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            json = response.json()
            assert "_id" in json
            assert len(json["comments"]) == 1
