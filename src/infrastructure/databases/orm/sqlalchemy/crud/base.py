import typing

from sqlalchemy import Select
from sqlalchemy import bindparam
from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import update

from src.infrastructure.databases.orm.sqlalchemy import builders
from src.infrastructure.databases.orm.sqlalchemy import models
from src.infrastructure.databases.orm.sqlalchemy import tables
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.orm.sqlalchemy.utils import fetchall
from src.infrastructure.databases.orm.sqlalchemy.utils import fetchcount
from src.infrastructure.databases.orm.sqlalchemy.utils import fetchone


class Base(typing.Generic[tables.Table]):
    table: type[tables.Table]

    @classmethod
    def build(
        cls,
        statement: typing.Any,
        functions: list[models.Function] | None = None,
        filters: list[typing.Union[models.Filter, models.And, models.Or]] | None = None,
        sorting: list[models.Sorting] | None = None,
        pagination: models.Pagination | None = None,
    ) -> typing.Any:
        functions = [builders.Function.build(cls.table, model) for model in functions] if functions else []
        filters = [builders.Filter.build(cls.table, model) for model in filters] if filters else []
        sorting = [builders.Sorting.build(cls.table, model) for model in sorting] if sorting else []
        statement = builders.Pagination.build(statement, pagination) if pagination else statement
        statement = statement.order_by(*sorting) if isinstance(statement, Select) else statement  # type:ignore
        statement = statement.where(*filters, *functions)
        return statement

    @classmethod
    async def id(cls, session: Session) -> int:
        sequence = f"{cls.table.__tablename__}_id_seq"
        statement = text("SELECT nextval(:sequence)")
        return typing.cast(int, (await session.execute(statement, {"sequence": sequence})).scalar())

    @classmethod
    async def one(cls, session: Session, *filters: typing.Union[models.Filter, models.And, models.Or]) -> tables.Table:
        statement = cls.build(select(cls.table), filters=list(filters))
        return await fetchone(session, statement)

    @classmethod
    async def relations(
        cls,
        session: Session,
        *filters: typing.Union[models.Filter, models.And, models.Or],
    ) -> tables.Table:
        statement = cls.build(select(cls.table), filters=list(filters))
        return await fetchone(session, statement)

    @classmethod
    async def all(
        cls,
        session: Session,
        *filters: typing.Union[models.Filter, models.And, models.Or],
    ) -> list[tables.Table]:
        statement = cls.build(select(cls.table), filters=list(filters))
        return await fetchall(session, statement)

    @classmethod
    async def paginated(
        cls,
        session: Session,
        filters: list[typing.Union[models.Filter, models.And, models.Or]],
        sorting: list[models.Sorting],
        pagination: models.Pagination,
    ) -> tuple[list[tables.Table], int]:
        statement = cls.build(select(cls.table), filters=filters, sorting=sorting)
        rows = await fetchall(session, cls.build(statement, pagination=pagination))
        count = await fetchcount(session, statement)
        return rows, count

    @classmethod
    async def count(cls, session: Session, *filters: typing.Union[models.Filter, models.And, models.Or]) -> int:
        statement = cls.build(select(cls.table), filters=list(filters))
        return await fetchcount(session, statement)

    @classmethod
    async def exists(cls, session: Session, *filters: typing.Union[models.Filter, models.And, models.Or]) -> bool:
        statement = cls.build(exists(select(cls.table)), filters=list(filters))
        return bool((await session.execute(statement.select())).scalar())

    @classmethod
    async def create(cls, session: Session, row: dict[str, typing.Any]) -> tables.Table:
        columns = {k: v for k, v in row.items() if getattr(cls.table, k, None) is not None}
        instance = cls.table(**columns)
        session.add(instance)
        await session.flush()
        return instance

    @classmethod
    async def update(cls, session: Session, id: typing.Union[str, int], **kwargs: typing.Any) -> None:
        values = {key: bindparam(key) for key in kwargs if getattr(cls.table, key, None) is not None}
        statement = update(cls.table).where(cls.table.id == id).values(**values)  # type:ignore
        await session.execute(statement, kwargs)
        await session.flush()

    @classmethod
    async def delete(cls, session: Session, *filters: typing.Union[models.Filter, models.And, models.Or]) -> None:
        statement = cls.build(delete(cls.table), filters=list(filters))
        await session.execute(statement)
        await session.flush()


Crud = typing.TypeVar("Crud", bound=Base[typing.Any])
