# Code Implementer

## Changes

Добавлен production-сценарий поиска `accounts` в приватном HTTP-контуре.

Обновленные и новые файлы:

- `src/application/usecases/accounts/search.py`
- `src/entrypoints/http/system/deps/accounts/__init__.py`
- `src/entrypoints/http/system/deps/accounts/search.py`
- `src/entrypoints/http/system/routers/accounts/__init__.py`
- `src/entrypoints/http/system/routers/accounts/registry.py`
- `src/entrypoints/http/system/routers/accounts/search.py`
- `src/entrypoints/http/system/routers/registry.py`
- `src/entrypoints/http/system/schemas/accounts.py`
- `src/entrypoints/http/system/schemas/__init__.py`

## Code Artifacts

### `src/application/usecases/accounts/search.py`

```python
import typing

from src.application.utils import account
from src.decorators import sessionmaker
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.collections import Direction
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.queries import Pagination
from src.infrastructure.databases.orm.sqlalchemy.queries import Sorting
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption


class Container:
    def __init__(self, repository: Repository, security: Security) -> None:
        self.repository = repository
        self.security = security


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session), security=Security())

    @sessionmaker.read
    async def __call__(
        self,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[Account], int]:
        self.build(session)

        _filters: list[typing.Any] = []

        if filters.get("id"):
            _filters.append(Filter.eq(key="id", value=filters["id"]))

        _sorting = (
            [Sorting.asc("created")]
            if sorting.get("direction") == Direction.asc
            else [Sorting.desc("created")]
        )

        accounts, total = await self.container.repository.account.paginated(
            filters=_filters,
            sorting=_sorting,
            pagination=Pagination.page(limit=pagination["limit"], offset=pagination["offset"]),
        )

        return [
            account.decrypt(
                decrypter=self.container.security.encryption.decrypt,
                account=_account,
            )
            for _account in accounts
        ], total
```

### `src/entrypoints/http/system/schemas/accounts.py`

```python
import datetime
import typing

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

### `src/entrypoints/http/system/routers/accounts/search.py`

```python
from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.search import Usecase
from src.entrypoints.http.system.deps.accounts import dependency
from src.entrypoints.http.system.schemas import Accounts
from src.entrypoints.http.system.schemas import SearchAccount
from src.framework.routing import APIRouter


router = APIRouter()


@router.post(
    "/accounts:search",
    description="Search accounts",
    response_model=Accounts,
    status_code=status.HTTP_200_OK,
)
async def query(
    body: SearchAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Accounts:
    accounts, total = await usecase(**body.deserialize())
    return Accounts.serialize(accounts=accounts, total=total)
```

### `src/entrypoints/http/system/routers/registry.py`

```python
from src.framework.routing import APIRouter
from fastapi import Depends

from src.entrypoints.http.common.deps import basic

from . import accounts


router = APIRouter(prefix="/api/-")


router.include_router(accounts.router, tags=["Accounts"], dependencies=[Depends(basic)])
```

## Checks

### `python3 -m compileall src/application/usecases/accounts src/entrypoints/http/system`

Passed.

### `python3 .scripts/lints/run.py lint --path .`

Failed.

```text
ModuleNotFoundError: No module named 'typer'
```

`python .scripts/lints/run.py` from agent instructions was attempted through `python3` because only that interpreter is available in the environment.
