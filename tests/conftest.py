from typing import Callable, AsyncGenerator
import asyncio
from _pytest import mark

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

TestClientGenerator = Callable[[FastAPI], AsyncGenerator[httpx.AsyncClient, None]]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
async def client(
    request: pytest.FixtureRequest,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    marker = request.node.get_closest_marker("fastapi")
    if marker is None:
        raise ValueError("client fixture: the marker fastapi must be provided")
    try:
        app = marker.kwargs["app"]
    except KeyError:
        raise ValueError(
            "client fixture: keyword argument app must be provided in the marker"
        )
    if not isinstance(app, FastAPI):
        raise ValueError("client fixture: app must be a FastAPI instance")

    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client
