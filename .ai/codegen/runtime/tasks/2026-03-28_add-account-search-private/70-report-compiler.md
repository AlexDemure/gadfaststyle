# Final Report

## Business Requirement

`Добавь ручку :search в приватные ручки для сущности accounts с пагинацией с сортировкой по полю created, с возможность desc\asc и точному фильтру по полю id.`

## Architect Todo List

| Status | Executor | Description |
|---|---|---|
| done | 40-code-implementer | Добавить `src/application/usecases/accounts/search.py` с пагинацией, сортировкой по `created` и точным фильтром по `id`. |
| done | 40-code-implementer | Подключить приватную ручку `POST /api/-/accounts:search` через `src/entrypoints/http/system/deps/accounts/search.py`, `src/entrypoints/http/system/routers/accounts/search.py`, `src/entrypoints/http/system/routers/accounts/registry.py`. |
| done | 40-code-implementer | Добавить системные схемы `SearchAccount` и `Accounts` в `src/entrypoints/http/system/schemas/accounts.py` и экспортировать их через `src/entrypoints/http/system/schemas/__init__.py`. |
| done | 50-test-writer | Добавить интеграционные тесты на сортировку `created` desc/asc, точный фильтр по `id`, пагинацию и basic auth в `tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_search.py`. |
| blocked | 40-code-implementer, 50-test-writer | Прогнать `python .scripts/lints/run.py` и зафиксировать результат. |
| done | 60-code-reviewer | Проверить реализацию на регрессии маршрутизации, корректность контракта схем и тестовые пробелы. |
| done | 41-code-implementer, 61-code-reviewer | Перевести `accounts:search` с generic `paginated(...)` на отдельные `adapter.search(...)` и `crud.search(...)`, а `decrypt` вынести в отдельный шаг перед `return`. |

## Execution History

### 10-delivery-manager

```md
# Delivery Manager

## Request

`Задача: Добавь ручку :search в приватные ручки для сущности accounts с пагинацией с сортировкой по полю created, с возможность desc\asc и точному фильтру по полю id.`

## Scope

- Добавить приватную HTTP-ручку `accounts:search`.
- Провести изменение по конвейеру отчетов.
- Подтвердить кодом пагинацию, сортировку по `created` и точный фильтр по `id`.
```

### 20-project-architect

```md
## Architecture Context

Сценарий относится к приватному HTTP-контуру `src/entrypoints/http/system`. Для него уже используется общий router registry с `basic` authentication на префиксе `/api/-`. Для `accounts` ранее уже существовал доменный срез в `application/usecases/accounts`, а в `system`-контуре остались точки интеграции через `deps`, `routers`, `schemas` и зеркальные интеграционные тесты.

Путь данных для новой выборки:

`SearchAccount schema -> system dependency -> system router /accounts:search -> application usecase -> postgres adapter repository.paginated(...) -> response schema`
```

### 30-task-orchestrator

```md
1. Проверить существующий `system` HTTP-контур для `accounts` и определить, какие файлы нужно добавить или обновить для `search`.
2. Добавить usecase поиска аккаунтов с:
   - точным фильтром по `id`
   - сортировкой по `created`
   - переключением `asc` / `desc`
   - пагинацией через общий `Pagination.page(...)`
3. Добавить системные request/response схемы для `accounts:search`.
4. Подключить dependency и router в `system` registry.
5. Добавить интеграционные тесты.
```

### 40-code-implementer

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

```text
python3 -m compileall src/application/usecases/accounts src/entrypoints/http/system
# passed

python3 .scripts/lints/run.py lint --path .
ModuleNotFoundError: No module named 'typer'
```

### 41-code-implementer

```python
    @sessionmaker.read
    async def __call__(
        self,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[Account], int]:
        self.build(session)

        accounts, total = await self.container.repository.account.search(
            filters=filters,
            sorting=sorting,
            pagination=pagination,
        )

        accounts = [
            account.decrypt(
                decrypter=self.container.security.encryption.decrypt,
                account=_account,
            )
            for _account in accounts
        ]

        return accounts, total
```

```python
    @classmethod
    async def search(
        cls,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[tables.Account], int]:
        statement = select(cls.table)

        if filters.get("id"):
            statement = statement.where(cls.table.id == filters["id"])

        if sorting.get("direction") is Direction.asc:
            statement = statement.order_by(asc(cls.table.created), desc(cls.table.id))
        else:
            statement = statement.order_by(desc(cls.table.created), desc(cls.table.id))
```

### 50-test-writer

```python
class TestAccountsSearch:
    @pytest.mark.asyncio
    async def test_desc(self) -> None:
        first_id, second_id = await self.given()

        response = await self.when(direction="desc")

        assert response["total"] == 2
        assert [item["id"] for item in response["items"]] == [second_id, first_id]
        assert [item["external_id"] for item in response["items"]] == ["second-user", "first-user"]

    @pytest.mark.asyncio
    async def test_asc(self) -> None:
        first_id, second_id = await self.given()

        response = await self.when(direction="asc")

        assert response["total"] == 2
        assert [item["id"] for item in response["items"]] == [first_id, second_id]

    @pytest.mark.asyncio
    async def test_filter_by_id(self) -> None:
        _, second_id = await self.given()

        response = await self.when(account_id=second_id)

        assert response["total"] == 1
        assert [item["id"] for item in response["items"]] == [second_id]
```

```text
pytest tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_search.py -q
bash: line 1: pytest: command not found

python3 .scripts/lints/run.py lint --path .
ModuleNotFoundError: No module named 'typer'
```

### 60-code-reviewer

```md
## Findings

Функциональных замечаний по добавленной ручке не выявлено.

## Residual Risks

- Автопроверка тестов не была выполнена из-за отсутствия `pytest` в окружении.
- Линтерный сценарий не выполнен до конца из-за отсутствия зависимости `typer`.
```

### 61-code-reviewer

```md
## Findings

После корректировки паттерн `search` теперь соответствует архитектурному правилу:

- usecase больше не собирает query-builder объекты
- business `:search` идет через отдельные `adapter.search(...)` и `crud.search(...)`
- пост-обработка `decrypt` вынесена в отдельный шаг перед `return`
```

## Outcome

Добавлена приватная ручка `POST /api/-/accounts:search` с:

- пагинацией
- сортировкой по `created` с поддержкой `asc` и `desc`
- точным фильтром по `id`
- отдельными `adapter.search(...)` и `crud.search(...)` вместо generic `paginated(...)`
- интеграционным тестовым покрытием на основной сценарий и unauthorized доступ

## Verification

- `python3 -m compileall src/application/usecases/accounts src/entrypoints/http/system tests/test_integrations/test_entrypoints/test_http/test_system` - passed
- `python3 .scripts/lints/run.py lint --path .` - blocked, отсутствует `typer`
- `pytest tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_search.py -q` - blocked, отсутствует `pytest`
