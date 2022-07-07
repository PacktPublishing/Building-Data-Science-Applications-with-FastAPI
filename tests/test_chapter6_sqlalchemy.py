import os
from typing import Any, Dict, Optional

import httpx
import pytest
import pytest_asyncio
import sqlalchemy
from databases import Database
from fastapi import status

from chapter6.sqlalchemy.app import app
from chapter6.sqlalchemy.models import PostDB, metadata, posts
from chapter6.sqlalchemy.database import get_database


DATABASE_FILE_PATH = "chapter6_sqlalchemy.test.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE_PATH}"
database_test = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initialize_database():
    metadata.create_all(sqlalchemy_engine)

    initial_posts = [
        PostDB(id=1, title="Post 1", content="Content 1"),
        PostDB(id=2, title="Post 2", content="Content 2"),
        PostDB(id=3, title="Post 3", content="Content 3"),
    ]
    insert_query = posts.insert().values([post.dict() for post in initial_posts])
    await database_test.execute(insert_query)

    yield

    os.remove(DATABASE_FILE_PATH)


@pytest.mark.fastapi(
    app=app, dependency_overrides={get_database: lambda: database_test}
)
@pytest.mark.asyncio
class TestChapter6SQLAlchemy:
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
            (2, {"title": "Post 2 Updated"}, status.HTTP_200_OK),
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
