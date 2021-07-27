import asyncio
from typing import Optional, cast

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession
from starlette.websockets import WebSocketDisconnect

from chapter8.echo.app import app as chapter8_echo_app
from chapter8.concurrency.app import app as chapter8_concurrency_app
from chapter8.dependencies.app import app as chapter8_dependencies_app, API_TOKEN
from chapter8.broadcast.app import app as chapter8_broadcast_app


@pytest.mark.fastapi(app=chapter8_echo_app)
class TestChapter8Echo:
    def test_echo(self, websocket_client: TestClient):
        with websocket_client.websocket_connect("/ws") as websocket:
            websocket = cast(WebSocketTestSession, websocket)

            websocket.send_text("Hello")
            websocket.send_text("World")

            message1 = websocket.receive_text()
            message2 = websocket.receive_text()

            assert message1 == "Message text was: Hello"
            assert message2 == "Message text was: World"


@pytest.mark.fastapi(app=chapter8_concurrency_app)
class TestChapter8Concurrency:
    def test_echo(self, websocket_client: TestClient):
        with websocket_client.websocket_connect("/ws") as websocket:
            websocket = cast(WebSocketTestSession, websocket)

            message_time = websocket.receive_text()

            websocket.send_text("Hello")
            message_echo = websocket.receive_text()

            assert message_time.startswith("It is:")
            assert message_echo == "Message text was: Hello"


@pytest.mark.fastapi(app=chapter8_dependencies_app)
class TestChapter8Dependencies:
    def test_missing_token(self, websocket_client: TestClient):
        with pytest.raises(WebSocketDisconnect) as e:
            websocket_client.websocket_connect("/ws")
            assert e.value.code == status.WS_1008_POLICY_VIOLATION

    def test_invalid_token(self, websocket_client: TestClient):
        with pytest.raises(WebSocketDisconnect) as e:
            websocket_client.websocket_connect(
                "/ws", headers={"Cookie": f"token=INVALID_TOKEN"}
            )
            assert e.value.code == status.WS_1008_POLICY_VIOLATION

    @pytest.mark.parametrize(
        "username,welcome_message",
        [(None, "Hello, Anonymous!"), ("John", "Hello, John!")],
    )
    def test_valid_token(
        self,
        websocket_client: TestClient,
        username: Optional[str],
        welcome_message: str,
    ):
        url = "/ws"
        if username:
            url += f"?username={username}"

        with websocket_client.websocket_connect(
            url, headers={"Cookie": f"token={API_TOKEN}"}
        ) as websocket:
            websocket = cast(WebSocketTestSession, websocket)

            message1 = websocket.receive_text()

            websocket.send_text("Hello")
            message2 = websocket.receive_text()

            assert message1 == welcome_message
            assert message2 == "Message text was: Hello"


@pytest.mark.fastapi(app=chapter8_broadcast_app)
@pytest.mark.skip
class TestChapter8Broadcast:
    def test_broadcast(self, websocket_client: TestClient):
        with websocket_client.websocket_connect("/ws?username=U1") as websocket1:
            with websocket_client.websocket_connect("/ws?username=U2") as websocket2:
                websocket1 = cast(WebSocketTestSession, websocket1)
                websocket2 = cast(WebSocketTestSession, websocket2)

                websocket1.send_text("Hello from U1")
                websocket2.send_text("Hello from U2")

                websocket2_message = websocket2.receive_json()
                websocket1_message = websocket1.receive_json()

                assert websocket2_message == {
                    "username": "U1",
                    "message": "Hello from U1",
                }
                assert websocket1_message == {
                    "username": "U2",
                    "message": "Hello from U2",
                }
