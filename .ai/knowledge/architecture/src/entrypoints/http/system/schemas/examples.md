## Эталонная форма

```python
import typing
import datetime

from src.common.formats.utils import field
from src.domain import models
from src.entrypoints.http.common.schemas import Paginated
from src.entrypoints.http.common.schemas import Pagination
from src.entrypoints.http.common.schemas import Query
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response
from src.infrastructure.databases.orm.sqlalchemy.collections import Direction

from .base import System


class SearchAccount(System, Request, Query):
    class SearchAccountFilters(System, Request, Query):
        id: int | None = None

    class SearchAccountSorting(System, Request, Query):
        direction: Direction = Direction.desc

    class SearchAccountPagination(System, Request, Query, Pagination): ...

    filters: SearchAccountFilters
    sorting: SearchAccountSorting
    pagination: SearchAccountPagination

    def deserialize(self) -> dict[str, typing.Any]:
        data = self.model_dump()
        data["pagination"] = self.pagination.convert
        return data


class Account(System, Response):
    id: int
    external_id: str
    created: datetime.datetime

    @classmethod
    def serialize(cls, account: models.Account) -> typing.Self:
        return cls(
            id=field.required(account.id),
            external_id=account.external_id,
            created=account.created,
        )


class Accounts(System, Paginated, Response):
    items: list[Account]

    @classmethod
    def serialize(cls, accounts: list[models.Account], total: int) -> typing.Self:
        return cls(
            total=total,
            items=[Account.serialize(account) for account in accounts],
        )
```
