import httpx
import pytest
from fastapi import status

from chapter7.cors.app_without_cors import app as app_without_cors
from chapter7.cors.app_with_cors import app as app_with_cors


@pytest.mark.fastapi(app=app_without_cors)
@pytest.mark.asyncio
class TestChapter7AppWithoutCORS:
    async def test_options(self, client: httpx.AsyncClient):
        response = await client.options("/")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    async def test_get(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"detail": "GET response"}

        assert "access-control-allow-origin" not in response.headers

    async def test_post(self, client: httpx.AsyncClient):
        response = await client.post("/", json={"hello": "world"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"detail": "POST response", "input_payload": {"hello": "world"}}

        assert "access-control-allow-origin" not in response.headers


@pytest.mark.fastapi(app=app_with_cors)
@pytest.mark.asyncio
class TestChapter7AppWithCORS:
    async def test_options(self, client: httpx.AsyncClient):
        response = await client.options(
            "/",
            headers={
                "Origin": "http://localhost:9000",
                "access-control-request-method": "POST",
            },
        )

        assert response.status_code == status.HTTP_200_OK

        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:9000"
        )

    async def test_get(self, client: httpx.AsyncClient):
        response = await client.get("/", headers={"Origin": "http://localhost:9000"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"detail": "GET response"}

        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:9000"
        )

    async def test_post(self, client: httpx.AsyncClient):
        response = await client.post(
            "/", headers={"Origin": "http://localhost:9000"}, json={"hello": "world"}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"detail": "POST response", "input_payload": {"hello": "world"}}

        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:9000"
        )
