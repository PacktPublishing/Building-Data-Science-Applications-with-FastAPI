from typing import Any, Dict, Optional

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
from chapter3.chapter3_request_body_01 import (
    app as chapter3_request_body_01_app,
)
from chapter3.chapter3_request_body_02 import (
    app as chapter3_request_body_02_app,
)
from chapter3.chapter3_request_body_03 import (
    app as chapter3_request_body_03_app,
)
from chapter3.chapter3_request_body_04 import (
    app as chapter3_request_body_04_app,
)
from chapter3.chapter3_form_data_01 import (
    app as chapter3_form_data_01_app,
)
from chapter3.chapter3_file_uploads_01 import (
    app as chapter3_file_uploads_01_app,
)
from chapter3.chapter3_file_uploads_02 import (
    app as chapter3_file_uploads_02_app,
)
from chapter3.chapter3_file_uploads_03 import (
    app as chapter3_file_uploads_03_app,
)
from chapter3.chapter3_headers_cookies_01 import (
    app as chapter3_headers_cookies_01_app,
)
from chapter3.chapter3_headers_cookies_02 import (
    app as chapter3_headers_cookies_02_app,
)
from chapter3.chapter3_headers_cookies_03 import (
    app as chapter3_headers_cookies_03_app,
)
from chapter3.chapter3_request_object_01 import (
    app as chapter3_request_object_01_app,
)
from chapter3.chapter3_response_path_parameters_01 import (
    app as chapter3_response_path_parameters_01_app,
)
from chapter3.chapter3_response_path_parameters_02 import (
    app as chapter3_response_path_parameters_02_app,
)
from chapter3.chapter3_response_path_parameters_03 import (
    app as chapter3_response_path_parameters_03_app,
)
from chapter3.chapter3_response_path_parameters_04 import (
    app as chapter3_response_path_parameters_04_app,
)
from chapter3.chapter3_response_parameter_01 import (
    app as chapter3_response_parameter_01_app,
)
from chapter3.chapter3_response_parameter_02 import (
    app as chapter3_response_parameter_02_app,
)
from chapter3.chapter3_response_parameter_03 import (
    app as chapter3_response_parameter_03_app,
)
from chapter3.chapter3_raise_errors_01 import (
    app as chapter3_raise_errors_01_app,
)
from chapter3.chapter3_raise_errors_02 import (
    app as chapter3_raise_errors_02_app,
)
from chapter3.chapter3_custom_response_01 import (
    app as chapter3_custom_response_01_app,
)
from chapter3.chapter3_custom_response_02 import (
    app as chapter3_custom_response_02_app,
)
from chapter3.chapter3_custom_response_03 import (
    app as chapter3_custom_response_03_app,
)
from chapter3.chapter3_custom_response_04 import (
    app as chapter3_custom_response_04_app,
)
from chapter3.chapter3_custom_response_05 import (
    app as chapter3_custom_response_05_app,
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
        response = await client.get("/users/standard/123/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"type": "standard", "id": 123}


@pytest.mark.fastapi(app=chapter3_path_parameters_03_app)
@pytest.mark.asyncio
class TestPathParameters03:
    async def test_get_invalid_type(self, client: httpx.AsyncClient):
        response = await client.get("/users/foo/123/")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("type", ["standard", "admin"])
    async def test_get_standard_user(self, client: httpx.AsyncClient, type: str):
        response = await client.get(f"/users/{type}/123/")

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
    async def test_get_out_of_range_parameters(
        self, client: httpx.AsyncClient, page: int, size: int
    ):
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


@pytest.mark.fastapi(app=chapter3_request_body_01_app)
@pytest.mark.asyncio
class TestRequestBody01:
    @pytest.mark.parametrize(
        "payload", [{}, {"name": "John"}, {"name": "John", "age": "Doe"}]
    )
    async def test_get_wrong_payload(
        self, client: httpx.AsyncClient, payload: Dict[str, Any]
    ):
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_payload(self, client: httpx.AsyncClient):
        payload = {"name": "John", "age": 30}
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_request_body_02_app)
@pytest.mark.asyncio
class TestRequestBody02:
    @pytest.mark.parametrize(
        "payload", [{}, {"name": "John"}, {"name": "John", "age": "Doe"}]
    )
    async def test_get_wrong_payload(
        self, client: httpx.AsyncClient, payload: Dict[str, Any]
    ):
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_payload(self, client: httpx.AsyncClient):
        payload = {"name": "John", "age": 30}
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_request_body_03_app)
@pytest.mark.asyncio
class TestRequestBody03:
    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"user": {}, "company": {}},
            {"user": {"name": "John", "age": "Doe"}, "company": {"name": "ACME"}},
        ],
    )
    async def test_get_wrong_payload(
        self, client: httpx.AsyncClient, payload: Dict[str, Any]
    ):
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_payload(self, client: httpx.AsyncClient):
        payload = {"user": {"name": "John", "age": 30}, "company": {"name": "ACME"}}
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_request_body_04_app)
@pytest.mark.asyncio
class TestRequestBody04:
    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"user": {}, "priority": "foo"},
            {"user": {"name": "John", "age": "Doe"}, "priority": 1},
            {"user": {"name": "John", "age": 30}, "priority": 0},
        ],
    )
    async def test_get_wrong_payload(
        self, client: httpx.AsyncClient, payload: Dict[str, Any]
    ):
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_payload(self, client: httpx.AsyncClient):
        payload = {"user": {"name": "John", "age": 30}, "priority": 1}
        response = await client.post("/users", json=payload)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_form_data_01_app)
@pytest.mark.asyncio
class TestFormData01:
    @pytest.mark.parametrize(
        "payload", [{}, {"name": "John"}, {"name": "John", "age": "Doe"}]
    )
    async def test_get_wrong_payload(
        self, client: httpx.AsyncClient, payload: Dict[str, Any]
    ):
        response = await client.post("/users", data=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_payload(self, client: httpx.AsyncClient):
        payload = {"name": "John", "age": 30}
        response = await client.post("/users", data=payload)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_file_uploads_01_app)
@pytest.mark.asyncio
class TestFileUploads01:
    async def test_get_missing_file(self, client: httpx.AsyncClient):
        response = await client.post("/files")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_file(self, client: httpx.AsyncClient):
        response = await client.post("/files", files={"file": b"Hello"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"file_size": 5}


@pytest.mark.fastapi(app=chapter3_file_uploads_02_app)
@pytest.mark.asyncio
class TestFileUploads02:
    async def test_get_missing_file(self, client: httpx.AsyncClient):
        response = await client.post("/files")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_file(self, client: httpx.AsyncClient):
        response = await client.post("/files", files={"file": ("hello.txt", b"Hello")})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"file_name": "hello.txt", "content_type": "text/plain"}


@pytest.mark.fastapi(app=chapter3_file_uploads_03_app)
@pytest.mark.asyncio
class TestFileUploads03:
    async def test_get_missing_files(self, client: httpx.AsyncClient):
        response = await client.post("/files")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_get_valid_files(self, client: httpx.AsyncClient):
        response = await client.post(
            "/files",
            files=[
                ("files", ("hello1.txt", b"Hello")),
                ("files", ("hello2.txt", b"Hello")),
            ],
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == [
            {"file_name": "hello1.txt", "content_type": "text/plain"},
            {"file_name": "hello2.txt", "content_type": "text/plain"},
        ]


@pytest.mark.fastapi(app=chapter3_headers_cookies_01_app)
@pytest.mark.asyncio
class TestHeadersCookies01:
    async def test_missing_header(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_header(self, client: httpx.AsyncClient):
        response = await client.get("/", headers={"Hello": "World"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "World"}


@pytest.mark.fastapi(app=chapter3_headers_cookies_02_app)
@pytest.mark.asyncio
class TestHeadersCookies02:
    async def test_missing_header(self, client: httpx.AsyncClient):
        client.headers.pop("User-Agent")
        response = await client.get("/")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_header(self, client: httpx.AsyncClient):
        response = await client.get("/", headers={"User-Agent": "HTTPX"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"user_agent": "HTTPX"}


@pytest.mark.fastapi(app=chapter3_headers_cookies_03_app)
@pytest.mark.asyncio
class TestHeadersCookies03:
    @pytest.mark.parametrize("cookie", [None, "World"])
    async def test_cookie(self, client: httpx.AsyncClient, cookie: Optional[str]):
        cookies = []
        if cookie:
            cookies.append(("hello", cookie))
        response = await client.get("/", cookies=cookies)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": cookie}


@pytest.mark.fastapi(app=chapter3_request_object_01_app)
@pytest.mark.asyncio
class TestRequestObject01:
    async def test_request(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"path": "/"}


@pytest.mark.fastapi(app=chapter3_response_path_parameters_01_app)
@pytest.mark.asyncio
class TestResponsePathParameters01:
    async def test_create_post(self, client: httpx.AsyncClient):
        payload = {"title": "Hello"}
        response = await client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_response_path_parameters_02_app)
@pytest.mark.asyncio
class TestResponsePathParameters02:
    async def test_delete_post(self, client: httpx.AsyncClient):
        response = await client.delete("/posts/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        json = response.json()
        assert json == None


@pytest.mark.fastapi(app=chapter3_response_path_parameters_03_app)
@pytest.mark.asyncio
class TestResponsePathParameters03:
    async def test_get_post(self, client: httpx.AsyncClient):
        response = await client.get("/posts/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"title": "Hello", "nb_views": 100}


@pytest.mark.fastapi(app=chapter3_response_path_parameters_04_app)
@pytest.mark.asyncio
class TestResponsePathParameters04:
    async def test_get_post(self, client: httpx.AsyncClient):
        response = await client.get("/posts/1")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"title": "Hello"}


@pytest.mark.fastapi(app=chapter3_response_parameter_01_app)
@pytest.mark.asyncio
class TestResponseParameter01:
    async def test_get(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["custom-header"] == "Custom-Header-Value"
        json = response.json()
        assert json == {"hello": "world"}


@pytest.mark.fastapi(app=chapter3_response_parameter_02_app)
@pytest.mark.asyncio
class TestResponseParameter02:
    async def test_get(self, client: httpx.AsyncClient):
        response = await client.get("/")

        assert response.status_code == status.HTTP_200_OK
        assert response.cookies["cookie-name"] == "cookie-value"
        json = response.json()
        assert json == {"hello": "world"}


@pytest.mark.fastapi(app=chapter3_response_parameter_03_app)
@pytest.mark.asyncio
class TestResponseParameter03:
    @pytest.mark.parametrize(
        "id,status_code", [(1, status.HTTP_200_OK), (2, status.HTTP_201_CREATED)]
    )
    async def test_update_or_create(
        self, client: httpx.AsyncClient, id: int, status_code: int
    ):
        payload = {"title": "New title"}
        response = await client.put(f"/posts/{id}", json=payload)

        assert response.status_code == status_code
        json = response.json()
        assert json == payload


@pytest.mark.fastapi(app=chapter3_raise_errors_01_app)
@pytest.mark.asyncio
class TestRaiseErrors01:
    @pytest.mark.parametrize(
        "password,password_confirm,status_code,message",
        [
            (
                "aa",
                "bb",
                status.HTTP_400_BAD_REQUEST,
                {"detail": "Passwords don't match."},
            ),
            ("aa", "aa", status.HTTP_200_OK, {"message": "Passwords match."}),
        ],
    )
    async def test_check_password(
        self,
        client: httpx.AsyncClient,
        password: str,
        password_confirm: str,
        status_code: int,
        message: Dict[str, str],
    ):
        payload = {"password": password, "password_confirm": password_confirm}
        response = await client.post(f"/password", json=payload)

        assert response.status_code == status_code
        json = response.json()
        assert json == message


@pytest.mark.fastapi(app=chapter3_raise_errors_02_app)
@pytest.mark.asyncio
class TestRaiseErrors02:
    @pytest.mark.parametrize(
        "password,password_confirm,status_code,message",
        [
            (
                "aa",
                "bb",
                status.HTTP_400_BAD_REQUEST,
                {
                    "detail": {
                        "message": "Passwords don't match.",
                        "hints": [
                            "Check the caps lock on your keyboard",
                            "Try to make the password visible by clicking on the eye icon to check your typing",
                        ],
                    }
                },
            ),
            ("aa", "aa", status.HTTP_200_OK, {"message": "Passwords match."}),
        ],
    )
    async def test_check_password(
        self,
        client: httpx.AsyncClient,
        password: str,
        password_confirm: str,
        status_code: int,
        message: Dict[str, str],
    ):
        payload = {"password": password, "password_confirm": password_confirm}
        response = await client.post(f"/password", json=payload)

        assert response.status_code == status_code
        json = response.json()
        assert json == message


@pytest.mark.fastapi(app=chapter3_custom_response_01_app)
@pytest.mark.asyncio
class TestCustomResponse01:
    async def test_html(self, client: httpx.AsyncClient):
        response = await client.get("/html")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        text = response.text
        assert text.strip().startswith("<html>")

    async def test_text(self, client: httpx.AsyncClient):
        response = await client.get("/text")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        text = response.text
        assert text == "Hello world!"


@pytest.mark.fastapi(app=chapter3_custom_response_02_app)
@pytest.mark.asyncio
class TestCustomResponse02:
    async def test_redirect(self, client: httpx.AsyncClient):
        response = await client.get("/redirect")

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/new-url"


@pytest.mark.fastapi(app=chapter3_custom_response_03_app)
@pytest.mark.asyncio
class TestCustomResponse03:
    async def test_redirect(self, client: httpx.AsyncClient):
        response = await client.get("/redirect")

        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
        assert response.headers["location"] == "/new-url"


@pytest.mark.fastapi(app=chapter3_custom_response_04_app)
@pytest.mark.asyncio
class TestCustomResponse04:
    async def test_cat(self, client: httpx.AsyncClient):
        response = await client.get("/cat")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "image/jpeg"
        assert response.headers["content-length"] == "71457"


@pytest.mark.fastapi(app=chapter3_custom_response_05_app)
@pytest.mark.asyncio
class TestCustomResponse05:
    async def test_xml(self, client: httpx.AsyncClient):
        response = await client.get("/xml")

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/xml"
        text = response.text
        assert text.strip().startswith("<?xml")
