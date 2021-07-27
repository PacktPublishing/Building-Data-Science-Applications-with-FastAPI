from os import path
from typing import cast

import httpx
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_unordered import unordered
from starlette.testclient import WebSocketTestSession

from chapter14.chapter14_api import app as chapter14_api_app
from chapter14.websocket_face_detection.app import (
    app as chapter14_websocket_face_detection_app,
)

assets_folder = path.join(path.dirname(path.dirname(__file__)), "assets")
people_image_file = path.join(assets_folder, "people.jpg")


@pytest.mark.fastapi(app=chapter14_api_app)
@pytest.mark.asyncio
class TestChapter14API:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/face-detection", files={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        response = await client.post(
            "/face-detection", files={"image": open(people_image_file, "rb")}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        faces = json["faces"]
        assert unordered(faces) == [[237, 92, 80, 80], [426, 75, 115, 115]]


@pytest.mark.fastapi(app=chapter14_websocket_face_detection_app)
class TestChapter14WebSocketFaceDetection:
    def test_single_detection(self, websocket_client: TestClient):
        with websocket_client.websocket_connect("/face-detection") as websocket:
            websocket = cast(WebSocketTestSession, websocket)

            with open(people_image_file, "rb") as image:
                websocket.send_bytes(image.read())
                result = websocket.receive_json()
                faces = result["faces"]
                assert unordered(faces) == [[237, 92, 80, 80], [426, 75, 115, 115]]

    def test_backpressure(self, websocket_client: TestClient):
        QUEUE_LIMIT = 10
        with websocket_client.websocket_connect("/face-detection") as websocket:
            websocket = cast(WebSocketTestSession, websocket)

            with open(people_image_file, "rb") as image:
                bytes = image.read()
                for _ in range(QUEUE_LIMIT + 1):
                    websocket.send_bytes(bytes)
                for _ in range(QUEUE_LIMIT):
                    result = websocket.receive_json()
                    faces = result["faces"]
                    assert unordered(faces) == [[237, 92, 80, 80], [426, 75, 115, 115]]
