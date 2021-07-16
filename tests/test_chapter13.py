from typing import List, Tuple

import httpx
import joblib
import pytest
from fastapi import status
from sklearn.pipeline import Pipeline
from chapter13.chapter13_prediction_endpoint import (
    app as chapter13_prediction_endpoint_app,
)
from chapter13.chapter13_caching import app as chapter13_caching_app, memory
from chapter13.chapter13_async_not_async import app as chapter13_async_not_async_app


def test_chapter13_dump_joblib():
    from chapter13.chapter13_dump_joblib import categories

    model_file = "newsgroups_model.joblib"
    loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
    model, targets = loaded_model

    assert isinstance(model, Pipeline)
    assert set(targets) == set(categories)


def test_chapter13_load_joblib():
    from chapter13.chapter13_load_joblib import model, targets

    assert isinstance(model, Pipeline)
    assert set(targets) == set(
        [
            "soc.religion.christian",
            "talk.religion.misc",
            "comp.sys.mac.hardware",
            "sci.crypt",
        ]
    )


@pytest.mark.fastapi(app=chapter13_prediction_endpoint_app)
@pytest.mark.asyncio
class TestChapter13PredictionEndpoint:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/prediction", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        response = await client.post(
            "/prediction", json={"text": "computer cpu memory ram"}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"category": "comp.sys.mac.hardware"}


@pytest.mark.fastapi(app=chapter13_caching_app)
@pytest.mark.asyncio
class TestChapter13Caching:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/prediction", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        memory.clear()

        for _ in range(2):
            response = await client.post(
                "/prediction", json={"text": "computer cpu memory ram"}
            )

            assert response.status_code == status.HTTP_200_OK
            json = response.json()
            assert json == {"category": "comp.sys.mac.hardware"}

    async def test_delete_cache(self, client: httpx.AsyncClient):
        response = await client.delete("/cache")

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.fastapi(app=chapter13_async_not_async_app)
@pytest.mark.asyncio
class TestChapter13AsyncNotAsync:
    @pytest.mark.parametrize("path", ["/fast", "/slow-async", "/slow-sync"])
    async def test_route(self, path: str, client: httpx.AsyncClient):
        response = await client.get(path)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"endpoint": path[1:]}
