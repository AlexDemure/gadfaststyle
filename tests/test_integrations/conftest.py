import typing

import pytest

from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.entrypoints.http import router
from src.infrastructure.databases.postgres import postgres

from tests.factories.infrastructure.databases.postgres import tables


@pytest.fixture(scope="module", autouse=True)
def app() -> typing.Generator[FastAPI, None, None]:
    postgres.start()
    application = FastAPI()
    application.include_router(router)
    yield application
    postgres.shutdown()


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> typing.AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
        yield _client


@pytest.fixture(scope="function")
async def session(app: FastAPI) -> typing.AsyncGenerator[AsyncSession, None]:
    connection = await postgres.orm.engine.connect()
    transaction = await connection.begin()
    sessionmaker = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(postgres.orm, "sessionmaker", sessionmaker)

    async with sessionmaker() as _session:
        for table in [tables.Account]:
            table._meta.sqlalchemy_session = _session

        try:
            yield _session
        finally:
            await _session.rollback()
            monkeypatch.undo()
            await transaction.rollback()
            await connection.close()
