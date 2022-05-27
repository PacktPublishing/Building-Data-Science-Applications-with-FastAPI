from typing import Callable, AsyncGenerator, Generator
import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi.testclient import TestClient

TestClientGenerator = Callable[[FastAPI], AsyncGenerator[httpx.AsyncClient, None]]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
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

    dependency_overrides = marker.kwargs.get("dependency_overrides")
    if dependency_overrides:
        if not isinstance(dependency_overrides, dict):
            raise ValueError(
                "client fixture: dependency_overrides must be a dictionary"
            )
        app.dependency_overrides = dependency_overrides

    run_lifespan_events = marker.kwargs.get("run_lifespan_events", True)
    if not isinstance(run_lifespan_events, bool):
        raise ValueError("client fixture: run_lifespan_events must be a bool")

    test_client_generator = httpx.AsyncClient(app=app, base_url="http://app.io")
    if run_lifespan_events:
        async with LifespanManager(app):
            async with test_client_generator as test_client:
                yield test_client
    else:
        async with test_client_generator as test_client:
            yield test_client


@pytest.fixture
def websocket_client(
    request: pytest.FixtureRequest,
    event_loop: asyncio.AbstractEventLoop,
) -> Generator[TestClient, None, None]:
    asyncio.set_event_loop(event_loop)

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

    dependency_overrides = marker.kwargs.get("dependency_overrides")
    if dependency_overrides:
        if not isinstance(dependency_overrides, dict):
            raise ValueError(
                "client fixture: dependency_overrides must be a dictionary"
            )
        app.dependency_overrides = dependency_overrides

    with TestClient(app) as test_client:
        yield test_client
