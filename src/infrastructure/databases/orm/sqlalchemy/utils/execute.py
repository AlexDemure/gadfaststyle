import typing

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.infrastructure.databases.orm.sqlalchemy.collections import ObjectNotFound
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.orm.sqlalchemy.tables import Table


async def fetchcount(session: Session, statement: typing.Any) -> int:
    return (await session.execute(select(func.count()).select_from(statement.subquery()))).scalars().one()


async def fetchone(session: Session, statement: typing.Any) -> Table:
    try:
        return typing.cast(Table, (await session.execute(statement)).scalars().one())
    except NoResultFound:
        raise ObjectNotFound


async def fetchall(session: Session, statement: typing.Any) -> list[Table]:
    return typing.cast(list[Table], (await session.execute(statement)).scalars().all())
