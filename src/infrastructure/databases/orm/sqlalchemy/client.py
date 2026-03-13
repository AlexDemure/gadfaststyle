import contextlib
import functools
import json
import typing

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.formats.encoders import JSONEncoder

from . import profilers
from .collections import ClientDisabled
from .collections import Isolation


class SQLAlchemy:
    def __init__(self, url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=False,
            future=True,
            isolation_level=Isolation.read_committed,
            json_serializer=functools.partial(json.dumps, cls=JSONEncoder, ensure_ascii=False),
        )
        self.sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(self.engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def read(self) -> typing.AsyncGenerator[AsyncSession, None]:
        if not self.sessionmaker:
            raise ClientDisabled

        async with self.sessionmaker() as session:
            profilers.execute(session)
            yield session

    @contextlib.asynccontextmanager
    async def write(self) -> typing.AsyncGenerator[AsyncSession, None]:
        if not self.sessionmaker:
            raise ClientDisabled

        async with self.sessionmaker() as session:
            profilers.execute(session)
            async with session.begin():
                yield session
