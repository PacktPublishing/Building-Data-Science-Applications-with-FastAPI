import httpx
import pytest
from fastapi import status

from chapter3_project.app import app
from chapter3_project.models.user import User
from chapter3_project.models.post import Post
from chapter3_project.db import db


@pytest.fixture(autouse=True)
def fill_db():
    db.users = {
        1: User(id=1, email="user1@example.com"),
        2: User(id=2, email="user2@example.com"),
        3: User(id=3, email="user3@example.com"),
    }
    db.posts = {
        1: Post(id=1, user=1, title="Post 1"),
        2: Post(id=2, user=2, title="Post 2"),
        3: Post(id=3, user=3, title="Post 3"),
    }


@pytest.mark.fastapi(app=app)
@pytest.mark.asyncio
class TestUsersRouter:
    async def test_all(self, client: httpx.AsyncClient):
        response = await client.get("/users/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) == 3

    async def test_get_not_found(self, client: httpx.AsyncClient):
        response = await client.get("/users/10")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_found(self, client: httpx.AsyncClient):
        response = await client.get("/users/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 1, "email": "user1@example.com"}

    async def test_create_invalid(self, client: httpx.AsyncClient):
        payload = {"foo": "bar"}
        response = await client.post("/users/", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_valid(self, client: httpx.AsyncClient):
        payload = {"email": "user4@example.com"}
        response = await client.post("/users/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == {"id": 4, "email": "user4@example.com"}
        assert 4 in db.users

    async def test_delete_not_found(self, client: httpx.AsyncClient):
        response = await client.delete("/users/10")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_found(self, client: httpx.AsyncClient):
        response = await client.delete("/users/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 1 not in db.users


@pytest.mark.fastapi(app=app)
@pytest.mark.asyncio
class TestPostsRouter:
    async def test_all(self, client: httpx.AsyncClient):
        response = await client.get("/posts/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) == 3

    async def test_get_not_found(self, client: httpx.AsyncClient):
        response = await client.get("/posts/10")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_found(self, client: httpx.AsyncClient):
        response = await client.get("/posts/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 1, "user": 1, "title": "Post 1"}

    async def test_create_invalid(self, client: httpx.AsyncClient):
        payload = {"title": "Post 4"}
        response = await client.post("/posts/", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_not_existing_user(self, client: httpx.AsyncClient):
        payload = {"user": 4, "title": "Post 4"}
        response = await client.post("/posts/", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        json = response.json()
        assert json == {"detail": "User with id 4 doesn't exist."}

    async def test_create_valid(self, client: httpx.AsyncClient):
        payload = {"user": 1, "title": "Post 4"}
        response = await client.post("/posts/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == {"id": 4, "user": 1, "title": "Post 4"}
        assert 4 in db.posts

    async def test_delete_not_found(self, client: httpx.AsyncClient):
        response = await client.delete("/posts/10")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_found(self, client: httpx.AsyncClient):
        response = await client.delete("/posts/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 1 not in db.posts
