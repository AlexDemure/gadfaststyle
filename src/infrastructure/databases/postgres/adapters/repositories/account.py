import typing

from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables

from .base import Base


class Account(Base[crud.Account, tables.Account, models.Account, exceptions.AccountNotFound]):
    crud = crud.Account
    table = tables.Account
    model = models.Account
    error = exceptions.AccountNotFound

    async def search(
        self,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[models.Account], int]:
        rows, total = await self.crud.search(
            session=self.session,
            filters=filters,
            sorting=sorting,
            pagination=pagination,
        )
        return [self.convert(row) for row in rows], total
