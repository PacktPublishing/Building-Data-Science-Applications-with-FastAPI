import os
from typing import Any, Dict, Optional

import httpx
import pytest
import pytest_asyncio
from fastapi import status
from tortoise import Tortoise

from chapter6.tortoise.app import app
from chapter6.tortoise.models import PostDB, PostTortoise


DATABASE_FILE_PATH = "chapter6_tortoise.test.db"
DATABASE_URL = f"sqlite://{DATABASE_FILE_PATH}"


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initialize_database():
    await Tortoise.init(
        db_url=DATABASE_URL, modules={"models": ["chapter6.tortoise.models"]}
    )
    await Tortoise.generate_schemas()

    initial_posts = [
        PostDB(id=1, title="Post 1", content="Content 1"),
        PostDB(id=2, title="Post 2", content="Content 2"),
        PostDB(id=3, title="Post 3", content="Content 3"),
    ]
    await PostTortoise.bulk_create(
        (PostTortoise(**post.dict()) for post in initial_posts)
    )

    yield

    await Tortoise.close_connections()
    os.remove(DATABASE_FILE_PATH)


@pytest.mark.fastapi(app=app, run_lifespan_events=False)
@pytest.mark.asyncio
class TestChapter6Tortoise:
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

    @pytest.mark.parametrize(
        "id,status_code", [(1, status.HTTP_200_OK), (10, status.HTTP_404_NOT_FOUND)]
    )
    async def test_get_post(self, client: httpx.AsyncClient, id: int, status_code: int):
        response = await client.get(f"/posts/{id}")

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            assert json["id"] == id

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
            assert "id" in json

    @pytest.mark.parametrize(
        "id,payload,status_code",
        [
            (1, {"title": "Post 1 Updated"}, status.HTTP_200_OK),
            (10, {"title": "Post 10 Updated"}, status.HTTP_404_NOT_FOUND),
        ],
    )
    async def test_update_post(
        self,
        client: httpx.AsyncClient,
        id: int,
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
        [(1, status.HTTP_204_NO_CONTENT), (10, status.HTTP_404_NOT_FOUND)],
    )
    async def test_delete_post(
        self, client: httpx.AsyncClient, id: int, status_code: int
    ):
        response = await client.delete(f"/posts/{id}")

        assert response.status_code == status_code
