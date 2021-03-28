import httpx
import pytest
from fastapi import status

from chapter3.chapter3_first_endpoint_01 import app as chapter3_first_endpoint_01_app
from chapter3.chapter3_path_parameters_01 import (
    app as chapter3_path_parameters_01_app,
)
from chapter3.chapter3_path_parameters_02 import (
    app as chapter3_path_parameters_02_app,
)
from chapter3.chapter3_path_parameters_03 import (
    app as chapter3_path_parameters_03_app,
)
from chapter3.chapter3_path_parameters_04 import (
    app as chapter3_path_parameters_04_app,
)
from chapter3.chapter3_path_parameters_05 import (
    app as chapter3_path_parameters_05_app,
)
from chapter3.chapter3_path_parameters_06 import (
    app as chapter3_path_parameters_06_app,
)
from chapter3.chapter3_query_parameters_01 import (
    app as chapter3_query_parameters_01_app,
)
from chapter3.chapter3_query_parameters_02 import (
    app as chapter3_query_parameters_02_app,
)
from chapter3.chapter3_query_parameters_03 import (
    app as chapter3_query_parameters_03_app,
)


@pytest.mark.fastapi(app=chapter3_first_endpoint_01_app)
@pytest.mark.asyncio
class TestFirstEndpoint01:
    async def test_get(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "world"}


@pytest.mark.fastapi(app=chapter3_path_parameters_01_app)
@pytest.mark.asyncio
class TestPathParameters01:
    async def test_get_without_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_str_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/abc")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_int_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/123")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 123}


@pytest.mark.fastapi(app=chapter3_path_parameters_02_app)
@pytest.mark.asyncio
class TestPathParameters02:
    async def test_get_company_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/standard/123")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"type": "standard", "id": 123}


@pytest.mark.fastapi(app=chapter3_path_parameters_03_app)
@pytest.mark.asyncio
class TestPathParameters03:
    async def test_get_invalid_type(self, client: httpx.AsyncClient):
        response = await client.get("/users/foo/123")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("type", ["standard", "admin"])
    async def test_get_standard_user(self, client: httpx.AsyncClient, type: str):
        response = await client.get(f"/users/{type}/123")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"type": type, "id": 123}


@pytest.mark.fastapi(app=chapter3_path_parameters_04_app)
@pytest.mark.asyncio
class TestPathParameters04:
    async def test_get_str_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/abc")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_zero_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_one_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 1}

    async def test_get_int_id(self, client: httpx.AsyncClient):
        response = await client.get("/users/123")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 123}


@pytest.mark.fastapi(app=chapter3_path_parameters_05_app)
@pytest.mark.asyncio
class TestPathParameters05:
    async def test_get_too_short(self, client: httpx.AsyncClient):
        response = await client.get("/license-plates/abc")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_too_long(self, client: httpx.AsyncClient):
        response = await client.get("/license-plates/abc-123-def")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_correct_length(self, client: httpx.AsyncClient):
        response = await client.get("/license-plates/ab-123-de")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"license": "ab-123-de"}


@pytest.mark.fastapi(app=chapter3_path_parameters_06_app)
@pytest.mark.asyncio
class TestPathParameters06:
    @pytest.mark.parametrize(
        "license", ["abc", "abc-123-def", "12-abc-42", "ab-123-bcd"]
    )
    async def test_get_invalid_format(self, client: httpx.AsyncClient, license: str):
        response = await client.get(f"/license-plates/{license}")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_format(self, client: httpx.AsyncClient):
        response = await client.get("/license-plates/ab-123-de")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"license": "ab-123-de"}


@pytest.mark.fastapi(app=chapter3_query_parameters_01_app)
@pytest.mark.asyncio
class TestQueryParameters01:
    async def test_get_wrong_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users", params={"page": "foo", "size": "bar"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_default_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 1, "size": 10}

    async def get_get_set_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users", params={"page": 5, "size": 100})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 5, "size": 100}


@pytest.mark.fastapi(app=chapter3_query_parameters_02_app)
@pytest.mark.asyncio
class TestQueryParameters02:
    async def test_missing_format(self, client: httpx.AsyncClient):
        response = await client.get("/users")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_wrong_format(self, client: httpx.AsyncClient):
        response = await client.get("/users", params={"format": "foo"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("format", ["short", "full"])
    async def test_acceptable_format(self, client: httpx.AsyncClient, format: str):
        response = await client.get("/users", params={"format": format})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"format": format}


@pytest.mark.fastapi(app=chapter3_query_parameters_03_app)
@pytest.mark.asyncio
class TestQueryParameters03:
    async def test_get_wrong_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users", params={"page": "foo", "size": "bar"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("page,size", [(0, 5), (1, 150), (0, 150)])
    async def test_get_out_of_range_parameters(self, client: httpx.AsyncClient, page: int, size: int):
        response = await client.get("/users", params={"page": page, "size": size})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_default_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 1, "size": 10}

    async def get_get_set_parameters(self, client: httpx.AsyncClient):
        response = await client.get("/users", params={"page": 5, "size": 100})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 5, "size": 100}
