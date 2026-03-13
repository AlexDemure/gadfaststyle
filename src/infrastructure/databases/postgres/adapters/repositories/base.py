import typing

from src.common.formats.utils import date
from src.common.typings.variables import Error
from src.domain.models import Model
from src.infrastructure.databases.orm.sqlalchemy.collections import ObjectNotFound
from src.infrastructure.databases.orm.sqlalchemy.crud import Crud
from src.infrastructure.databases.orm.sqlalchemy.models import And
from src.infrastructure.databases.orm.sqlalchemy.models import Filter
from src.infrastructure.databases.orm.sqlalchemy.models import Or
from src.infrastructure.databases.orm.sqlalchemy.models import Pagination
from src.infrastructure.databases.orm.sqlalchemy.models import Sorting
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.orm.sqlalchemy.tables import Table


class Base(typing.Generic[Crud, Table, Model, Error]):
    crud: type[Crud]
    table: type[Table]
    model: type[Model]
    error: type[Error]

    def __init__(self, session: Session):
        self.session = session

    def convert(self, table: Table) -> Model:
        return self.model(**table.__dict__)

    async def one(self, *filters: typing.Union[Filter, And, Or]) -> Model:
        try:
            row = await self.crud.one(self.session, *filters)
        except ObjectNotFound:
            raise self.error
        return self.convert(row)

    async def relations(self, *filters: typing.Union[Filter, And, Or]) -> Model:
        try:
            row = await self.crud.relations(self.session, *filters)
        except ObjectNotFound:
            raise self.error
        return self.convert(row)

    async def all(self, *filters: typing.Union[Filter, And, Or]) -> list[Model]:
        rows = await self.crud.all(self.session, *filters)
        return [self.convert(row) for row in rows]

    async def paginated(
        self,
        filters: list[typing.Union[Filter, And, Or]],
        sorting: list[Sorting],
        pagination: Pagination,
    ) -> tuple[list[Model], int]:
        rows, total = await self.crud.paginated(self.session, filters, sorting, pagination)
        return [self.convert(row) for row in rows], total

    async def count(self, *filters: typing.Union[Filter, And, Or]) -> int:
        return await self.crud.count(self.session, *filters)

    async def exists(self, *filters: typing.Union[Filter, And, Or]) -> bool:
        return await self.crud.exists(self.session, *filters)

    async def create(self, model: Model) -> Model:
        row = await self.crud.create(self.session, row=model.model_dump())
        return self.convert(row)

    async def update(self, id: typing.Union[str, int], **kwargs: typing.Any) -> None:
        await self.crud.update(session=self.session, id=id, updated=date.now(), **kwargs)

    async def delete(self, *filters: typing.Union[Filter, And, Or]) -> None:
        return await self.crud.delete(self.session, *filters)
