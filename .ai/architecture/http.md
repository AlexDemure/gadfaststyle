# Architecture: HTTP Layer

## Что входит в слой

- `src/entrypoints/http/public/schemas/`
- `src/entrypoints/http/public/deps/`
- `src/entrypoints/http/public/routers/`
- `src/entrypoints/http/*/registry.py`

## Структура нового домена

Если появляется новый домен, создавай отдельные директории по аналогии с `accounts`:

- `src/entrypoints/http/public/routers/<domain>/`
- `src/entrypoints/http/public/deps/<domain>/`

Каждая операция должна лежать в отдельном файле:

- `create.py`
- `delete.py`
- `current.py`
- `list.py`
- `update.py`

Папка домена должна иметь `registry.py`, который подключает роуты домена.

## Как подключать router

Сначала собирается router домена:

```python
# path: src/entrypoints/http/public/routers/accounts/registry.py
from src.framework.routing import APIRouter

from . import create
from . import current
from . import delete


router = APIRouter()

router.include_router(current.router)
router.include_router(create.router)
router.include_router(delete.router)
```

Потом домен подключается в общий registry:

```python
# path: src/entrypoints/http/public/routers/registry.py
from src.framework.routing import APIRouter

from . import accounts


router = APIRouter(prefix="/api")


router.include_router(accounts.router, tags=["Accounts"])
```

## Как писать endpoint

- В каждом файле операции создается `router = APIRouter()`.
- Обработчик обычно называется `command` для mutation и по текущему модулю повторяет стиль существующих ручек.
- Используй `Depends`, `Body`, `status`, `response_model`, `responses` в том же стиле, что и у `accounts`.
- Endpoint ничего не знает о БД и инфраструктуре напрямую, он только принимает схему и вызывает usecase.

Эталон формы:

```python
# path: src/entrypoints/http/public/routers/accounts/create.py
from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.create import Usecase
from src.domain.collections import AccountAlreadyExists
from src.entrypoints.http.public.deps.accounts.create import dependency
from src.entrypoints.http.public.schemas import CreateAccount
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter
from src.infrastructure.security.jwt.models import Tokens


router = APIRouter()


@router.post(
    "/accounts:create",
    description="Account create",
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED,
    responses=errors(AccountAlreadyExists),
)
async def command(usecase: Usecase = Depends(dependency), body: CreateAccount = Body(...)) -> Tokens:
    return await usecase(**body.deserialize())
```

## Как писать dependency

- DI-функция лежит рядом с доменом и операцией.
- Никакой сложной логики внутри dependency не нужно, если достаточно вернуть `Usecase()`.
- Называй фабрику `dependency`.

Пример:

```python
# path: src/entrypoints/http/public/deps/accounts/create.py
from src.application.usecases.accounts.create import Usecase


def dependency() -> Usecase:
    return Usecase()
```

## Как писать schema

- Схемы для одного домена группируй в одном модуле, если это уже соответствует текущему стилю.
- Для request используй базовые классы `Request`, `Command`.
- Для response используй `Response`.
- Имена схем строятся как `<Operation><Entity>`.

Пример:

```python
# path: src/entrypoints/http/public/schemas/accounts.py
import typing

from src.common.formats.utils import field
from src.domain.models import Account
from src.entrypoints.http.common.schemas import Command
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response

from .base import Public


class CreateAccount(Public, Request, Command):
    external_id: str


class CurrentAccount(Public, Response):
    id: int

    @classmethod
    def serialize(cls, account: Account) -> typing.Self:
        return cls(id=field.required(account.id))
```

## Что важно по стилю

- Не объединяй несколько операций в один router-файл.
- Не называй обработчики случайно, если рядом уже принят `command`.
- Не придумывай новый формат URL, если текущий домен использует `"/accounts:create"`.
- Если добавляется новый домен, подключи его через `registry.py`, иначе ручка не попадет в приложение.
