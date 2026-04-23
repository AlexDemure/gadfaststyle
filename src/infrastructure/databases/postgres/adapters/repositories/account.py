from src.domain import models
from src.domain.collections import AccountNotFound
from src.infrastructure.databases.orm.sqlalchemy.models import And
from src.infrastructure.databases.orm.sqlalchemy.models import Filter
from src.infrastructure.databases.orm.sqlalchemy.models import Or
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables
from src.infrastructure.databases.postgres.adapters.repositories.base import Base


class Account(Base[crud.Account, tables.Account, models.Account, AccountNotFound]):
    crud = crud.Account
    table = tables.Account
    model = models.Account
    error = AccountNotFound

    async def exists(self, *filters: Filter | And | Or) -> bool:
        return await self.crud.exists(self.session, *filters)
