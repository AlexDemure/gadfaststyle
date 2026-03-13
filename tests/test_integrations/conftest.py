import typing

import pytest

from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker as _sessionmaker

from src.configuration import settings
from src.entrypoints.http import router
from src.entrypoints.http.common.deps import read
from src.entrypoints.http.common.deps import write

from tests.factories.infrastructure.databases.postgres import tables


@pytest.fixture(scope="module", autouse=True)
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture(scope="module", autouse=True)
def engine() -> AsyncEngine:
    return create_async_engine(settings.POSTGRES_HOST, echo=False)


@pytest.fixture(scope="module", autouse=True)
async def sessionmaker(engine: AsyncEngine) -> typing.Any:
    return _sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)  # type:ignore


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine, sessionmaker: typing.Any) -> typing.AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as _session:
        try:
            yield _session
        finally:
            await _session.rollback()
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def factories(session: AsyncSession) -> None:
    for model in [tables.Account]:
        model._meta.sqlalchemy_session = session  # type:ignore


@pytest.fixture(scope="function")
async def client(app: FastAPI, session: AsyncSession) -> typing.AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[read] = lambda: session
    app.dependency_overrides[write] = lambda: session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
        yield _client
    app.dependency_overrides.clear()
