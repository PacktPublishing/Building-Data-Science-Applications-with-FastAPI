from typing import Optional

import httpx
import pytest
from fastapi import status

from chapter5.chapter5_what_is_dependency_injection_01 import (
    app as chapter5_what_is_dependency_injection_01_app,
)
from chapter5.chapter5_function_dependency_01 import (
    app as chapter5_function_dependency_01_app,
)
from chapter5.chapter5_function_dependency_02 import (
    app as chapter5_function_dependency_02_app,
)
from chapter5.chapter5_function_dependency_03 import (
    app as chapter5_function_dependency_03_app,
)
from chapter5.chapter5_class_dependency_01 import (
    app as chapter5_class_dependency_01_app,
)
from chapter5.chapter5_class_dependency_02 import (
    app as chapter5_class_dependency_02_app,
)
from chapter5.chapter5_path_dependency_01 import (
    app as chapter5_path_dependency_01_app,
)
from chapter5.chapter5_router_dependency_01 import (
    app as chapter5_router_dependency_01_app,
)
from chapter5.chapter5_router_dependency_02 import (
    app as chapter5_router_dependency_02_app,
)
from chapter5.chapter5_global_dependency_01 import (
    app as chapter5_global_dependency_01_app,
)


@pytest.mark.fastapi(app=chapter5_what_is_dependency_injection_01_app)
@pytest.mark.asyncio
class TestWhatIsDependencyInjection01:
    async def test_missing_header(self, client: httpx.AsyncClient):
        client.headers.pop("User-Agent")
        response = await client.get("/")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_header(self, client: httpx.AsyncClient):
        response = await client.get("/", headers={"User-Agent": "HTTPX"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"user_agent": "HTTPX"}


@pytest.mark.fastapi(app=chapter5_function_dependency_01_app)
@pytest.mark.parametrize("path", ["/items", "/things"])
@pytest.mark.asyncio
class TestFunctionDependency01:
    async def test_default_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 0, "limit": 10}

    async def test_custom_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": 10, "limit": 100})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 100}


@pytest.mark.fastapi(app=chapter5_function_dependency_02_app)
@pytest.mark.parametrize("path", ["/items", "/things"])
@pytest.mark.asyncio
class TestFunctionDependency02:
    async def test_default_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 0, "limit": 10}

    async def test_invalid_skip(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_invalid_limit(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"limit": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_capped_limit(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": 10, "limit": 1000})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 100}

    async def test_custom_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": 10, "limit": 100})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 100}


@pytest.mark.fastapi(app=chapter5_function_dependency_03_app)
@pytest.mark.asyncio
class TestFunctionDependency03:
    async def test_get_404(self, client: httpx.AsyncClient):
        response = await client.get("/posts/4")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_ok(self, client: httpx.AsyncClient):
        response = await client.get("/posts/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["id"] == 1

    async def test_update_404(self, client: httpx.AsyncClient):
        response = await client.patch("/posts/4", json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_ok(self, client: httpx.AsyncClient):
        response = await client.patch("/posts/1", json={"title": "New title"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json["id"] == 1
        assert json["title"] == "New title"

    async def test_delete_404(self, client: httpx.AsyncClient):
        response = await client.delete("/posts/4")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_ok(self, client: httpx.AsyncClient):
        response = await client.delete("/posts/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.fastapi(app=chapter5_class_dependency_01_app)
@pytest.mark.parametrize("path", ["/items", "/things"])
@pytest.mark.asyncio
class TestClassDependency01:
    async def test_default_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 0, "limit": 10}

    async def test_invalid_skip(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_invalid_limit(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"limit": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_capped_limit(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": 10, "limit": 1000})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 50}

    async def test_custom_pagination(self, client: httpx.AsyncClient, path: str):
        response = await client.get(path, params={"skip": 10, "limit": 50})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 50}


@pytest.mark.fastapi(app=chapter5_class_dependency_02_app)
@pytest.mark.asyncio
class TestClassDependency02:
    async def test_skip_limit_default_pagination(self, client: httpx.AsyncClient):
        response = await client.get("/items")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 0, "limit": 10}

    async def test_skip_limit_invalid_skip(self, client: httpx.AsyncClient):
        response = await client.get("/items", params={"skip": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_skip_limit_invalid_limit(self, client: httpx.AsyncClient):
        response = await client.get("/items", params={"limit": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_skip_limit_capped_limit(self, client: httpx.AsyncClient):
        response = await client.get("/items", params={"skip": 10, "limit": 1000})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 50}

    async def test_skip_limit_custom_pagination(self, client: httpx.AsyncClient):
        response = await client.get("/items", params={"skip": 10, "limit": 50})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"skip": 10, "limit": 50}

    async def test_page_size_default_pagination(self, client: httpx.AsyncClient):
        response = await client.get("/things")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 1, "size": 10}

    async def test_page_size_invalid_page(self, client: httpx.AsyncClient):
        response = await client.get("/things", params={"page": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_page_size_invalid_size(self, client: httpx.AsyncClient):
        response = await client.get("/things", params={"size": -10})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_page_size_capped_limit(self, client: httpx.AsyncClient):
        response = await client.get("/things", params={"page": 10, "size": 1000})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 10, "size": 50}

    async def test_page_size_custom_pagination(self, client: httpx.AsyncClient):
        response = await client.get("/things", params={"page": 10, "size": 50})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"page": 10, "size": 50}


@pytest.mark.fastapi(app=chapter5_path_dependency_01_app)
@pytest.mark.asyncio
class TestPathDependency01:
    @pytest.mark.parametrize("secret_header", [None, "INVALID_VALUE"])
    async def test_invalid_header(
        self, client: httpx.AsyncClient, secret_header: Optional[str]
    ):
        headers = {}
        if secret_header:
            headers["Secret-Header"] = secret_header
        response = await client.get("/protected-route", headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_header(self, client: httpx.AsyncClient):
        response = await client.get(
            "/protected-route", headers={"Secret-Header": "SECRET_VALUE"}
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.fastapi(app=chapter5_router_dependency_01_app)
@pytest.mark.parametrize("path", ["/router/route1", "/router/route2"])
@pytest.mark.asyncio
class TestRouterDependency01:
    @pytest.mark.parametrize("secret_header", [None, "INVALID_VALUE"])
    async def test_invalid_header(
        self, client: httpx.AsyncClient, path: str, secret_header: Optional[str]
    ):
        headers = {}
        if secret_header:
            headers["Secret-Header"] = secret_header
        response = await client.get(path, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_header(self, path: str, client: httpx.AsyncClient):
        response = await client.get(path, headers={"Secret-Header": "SECRET_VALUE"})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.fastapi(app=chapter5_router_dependency_02_app)
@pytest.mark.parametrize("path", ["/router/route1", "/router/route2"])
@pytest.mark.asyncio
class TestRouterDependency02:
    @pytest.mark.parametrize("secret_header", [None, "INVALID_VALUE"])
    async def test_invalid_header(
        self, client: httpx.AsyncClient, path: str, secret_header: Optional[str]
    ):
        headers = {}
        if secret_header:
            headers["Secret-Header"] = secret_header
        response = await client.get(path, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_header(self, path: str, client: httpx.AsyncClient):
        response = await client.get(path, headers={"Secret-Header": "SECRET_VALUE"})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.fastapi(app=chapter5_global_dependency_01_app)
@pytest.mark.parametrize("path", ["/route1", "/route2"])
@pytest.mark.asyncio
class TestGlobalDependency01:
    @pytest.mark.parametrize("secret_header", [None, "INVALID_VALUE"])
    async def test_invalid_header(
        self, client: httpx.AsyncClient, path: str, secret_header: Optional[str]
    ):
        headers = {}
        if secret_header:
            headers["Secret-Header"] = secret_header
        response = await client.get(path, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_header(self, path: str, client: httpx.AsyncClient):
        response = await client.get(path, headers={"Secret-Header": "SECRET_VALUE"})

        assert response.status_code == status.HTTP_200_OK
