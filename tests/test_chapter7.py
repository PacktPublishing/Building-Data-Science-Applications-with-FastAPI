import httpx
import pytest
from fastapi import status

from chapter7.chapter7_api_key_header import (
    app as chapter7_api_key_header_app,
    API_TOKEN as CHAPTER7_API_KEY_HEADER_API_TOKEN,
)
from chapter7.chapter7_api_key_header_dependency import (
    app as chapter7_api_key_header_app_dependency,
    API_TOKEN as CHAPTER7_API_KEY_HEADER_DEPENDENCY_API_TOKEN,
)


@pytest.mark.fastapi(app=chapter7_api_key_header_app)
@pytest.mark.asyncio
class TestChapter7APIKeyHeader:
    async def test_missing_header(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_invalid_token(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route", headers={"Token": "Foo"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_token(self, client: httpx.AsyncClient):
        response = await client.get(
            "/protected-route", headers={"Token": CHAPTER7_API_KEY_HEADER_API_TOKEN}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "world"}


@pytest.mark.fastapi(app=chapter7_api_key_header_app_dependency)
@pytest.mark.asyncio
class TestChapter7APIKeyHeaderDependency:
    async def test_missing_header(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_invalid_token(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route", headers={"Token": "Foo"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_token(self, client: httpx.AsyncClient):
        response = await client.get(
            "/protected-route",
            headers={"Token": CHAPTER7_API_KEY_HEADER_DEPENDENCY_API_TOKEN},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "world"}
