import asyncio

import pytest
from fastapi.testclient import TestClient

from chapter9.chapter9_websocket import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def websocket_client():
    with TestClient(app) as websocket_client:
        yield websocket_client


@pytest.mark.asyncio
async def test_websocket_echo(websocket_client: TestClient):
    with websocket_client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")

        message = websocket.receive_text()
        assert message == "Message text was: Hello"
