import runpy

import httpx
import pytest
from fastapi import status

from chapter4.chapter4_working_pydantic_objects_04 import (
    app as chapter4_working_pydantic_objects_04_app,
)
from chapter4.chapter4_working_pydantic_objects_05 import (
    app as chapter4_working_pydantic_objects_05_app,
    db,
    PostDB,
)


def test_chapter4():
    runpy.run_module("chapter4.chapter4_standard_field_types_01")
    runpy.run_module("chapter4.chapter4_standard_field_types_02")
    runpy.run_module("chapter4.chapter4_standard_field_types_03")
    runpy.run_module("chapter4.chapter4_optional_fields_default_values_01")
    runpy.run_module("chapter4.chapter4_optional_fields_default_values_02")
    runpy.run_module("chapter4.chapter4_fields_validation_01")
    runpy.run_module("chapter4.chapter4_fields_validation_02")
    runpy.run_module("chapter4.chapter4_pydantic_types_01")
    runpy.run_module("chapter4.chapter4_working_pydantic_objects_01")
    runpy.run_module("chapter4.chapter4_working_pydantic_objects_02")
    runpy.run_module("chapter4.chapter4_working_pydantic_objects_03")
    runpy.run_module("chapter4.chapter4_model_inheritance_01")
    runpy.run_module("chapter4.chapter4_model_inheritance_02")
    runpy.run_module("chapter4.chapter4_model_inheritance_03")
    runpy.run_module("chapter4.chapter4_custom_validation_01")
    runpy.run_module("chapter4.chapter4_custom_validation_02")
    runpy.run_module("chapter4.chapter4_custom_validation_03")


@pytest.mark.fastapi(app=chapter4_working_pydantic_objects_04_app)
@pytest.mark.asyncio
class TestWorkingPydanticObjects04:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/posts", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/posts", json={"title": "Foo", "content": "Bar"})

        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == {"id": 1, "title": "Foo", "content": "Bar"}


@pytest.mark.fastapi(app=chapter4_working_pydantic_objects_05_app)
@pytest.mark.asyncio
class TestWorkingPydanticObjects05:
    async def test_not_existing_post(self, client: httpx.AsyncClient):
        response = await client.patch("/posts/1", json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_valid_payload(self, client: httpx.AsyncClient):
        db.posts = {1: PostDB(id=1, title="Foo", content="Bar")}
        response = await client.patch("/posts/1", json={"title": "New title"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 1, "title": "New title", "content": "Bar"}
