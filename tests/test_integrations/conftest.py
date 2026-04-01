import typing

import pytest

from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient

from src.entrypoints.http import router


@pytest.fixture(scope="module", autouse=True)
def app() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> typing.AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
        yield _client
    app.dependency_overrides.clear()
