import typing

from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import postgres


async def dependency() -> typing.AsyncGenerator[Session, None]:
    async with postgres.orm.read() as session:
        yield session
