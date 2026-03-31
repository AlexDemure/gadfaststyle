# Project Architect: Update endpoint for accounts

## 1. Анализ архитектуры

**Слои и их роли:**

```
Router (entrypoints/http/public/routers/accounts/)
  └── Dep (entrypoints/http/public/deps/accounts/)
        └── Usecase (application/usecases/accounts/)
              └── Repository (infrastructure/databases/postgres/adapters/repositories/)
                    └── CRUD (infrastructure/databases/orm/sqlalchemy/crud/)
```

**Ключевые паттерны из существующего кода:**

1. `Usecase` — класс с методом `build(session)` и `__call__` задекорированным `@sessionmaker.write`
2. `dependency()` — простая функция без аргументов, возвращает `Usecase()`
3. Router регистрирует `Depends(dependency)` для usecase и `Depends(account)` для авторизации
4. `Base.update(id, **kwargs)` автоматически ставит `updated=date.now()` через репозиторий
5. Шифрование через `Account.encrypt(encrypter=..., external_id=...)` — используется в `create.py`
6. `Response` отдаёт `HTTP 204` через `response_class=Response` (FastAPI `Response`)

---

## 2. Зависимости между файлами

```
schemas/accounts.py          ← базовые классы Public, Request, Command
deps/accounts/update.py      ← usecases/accounts/update.py (Usecase)
routers/accounts/update.py   ← deps/accounts/update.py + schemas/__init__.py + common deps/account
                             ← usecases/accounts/update.py + domain/collections + common/collections
usecases/accounts/update.py  ← adapters/repositories/account.py + security/encryption
```

**Порядок создания** (от самого независимого к зависимому):
1. `src/application/usecases/accounts/update.py`
2. `src/entrypoints/http/public/deps/accounts/update.py`
3. `src/entrypoints/http/public/schemas/accounts.py` — добавить `UpdateAccount`
4. `src/entrypoints/http/public/routers/accounts/update.py`
5. Изменения в `__init__.py` и `registry.py`

---

## 3. Точный код для каждого файла

### 3.1 `src/application/usecases/accounts/update.py` (создать)

```python
from src.decorators import sessionmaker
from src.domain.models import Account
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

    @sessionmaker.write
    async def __call__(self, session: Session, account_id: int, external_id: str) -> None:
        self.build(session)

        await self.container.repository.account.update(
            id=account_id,
            **Account.encrypt(
                encrypter=self.container.security.encryption.encrypt,
                external_id=external_id,
            ),
        )
```

### 3.2 `src/entrypoints/http/public/deps/accounts/update.py` (создать)

```python
from src.application.usecases.accounts.update import Usecase


def dependency() -> Usecase:
    return Usecase()
```

### 3.3 `src/entrypoints/http/public/schemas/accounts.py` (изменить — добавить `UpdateAccount`)

Добавить в конец файла:

```python
class UpdateAccount(Public, Request, Command):
    external_id: str
```

### 3.4 `src/entrypoints/http/public/routers/accounts/update.py` (создать)

```python
from fastapi import Body
from fastapi import Depends
from fastapi import Response
from fastapi import status

from src.application.usecases.accounts.update import Usecase
from src.common.formats.utils import field
from src.domain.collections import AccountBlocked
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import account
from src.entrypoints.http.public.deps.accounts.update import dependency
from src.entrypoints.http.public.schemas import UpdateAccount
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.patch(
    "/accounts:update",
    description="Account update",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        **errors(
            *AUTHORIZATION_ERRORS,
            AccountNotFound,
            AccountBlocked,
        ),
    },
)
async def command(
    usecase: Usecase = Depends(dependency),
    _account: Account = Depends(account),
    body: UpdateAccount = Body(...),
) -> None:
    await usecase(account_id=field.required(_account.id), **body.deserialize())
```

---

## 4. Изменения в существующих файлах

### 4.1 `src/entrypoints/http/public/schemas/__init__.py`

Добавить экспорт `UpdateAccount`.

### 4.2 `src/entrypoints/http/public/routers/accounts/registry.py`

Добавить:
```python
from . import update
router.include_router(update.router)
```

---

## 5. Ожидаемое поведение и edge cases

**Нормальный flow:**
1. Клиент отправляет `PATCH /api/accounts:update` с заголовком `Authorization: Bearer <token>` и телом `{"external_id": "new_value"}`
2. `Depends(account)` — декодирует JWT, делает SELECT по account_id, проверяет blocked. Возвращает `Account`
3. Роутер вызывает `usecase(account_id=_account.id, external_id="new_value")`
4. Usecase шифрует `external_id`, вызывает `repository.account.update(id=account_id, external_id=<encrypted>)`
5. CRUD делает `UPDATE accounts SET external_id=:external_id, updated=:updated WHERE id=:id`
6. Возвращается `HTTP 204 No Content`

**Edge cases:**

| Случай | Что происходит |
|---|---|
| JWT отсутствует/невалиден | `Depends(account)` возвращает `HTTP 401` |
| Аккаунт заблокирован | `get.jwt.Usecase` бросает `AccountBlocked` |
| Аккаунт не найден в БД | `get.jwt.Usecase` бросает `AccountNotFound` |
| `_account.id` равен `None` | `field.required(_account.id)` бросает `ValueError` |
| Пользователь пытается обновить чужой аккаунт | Невозможно — `account_id` берётся из JWT |

---

## 6. Порядок создания файлов (итог)

1. `src/application/usecases/accounts/update.py`
2. `src/entrypoints/http/public/deps/accounts/update.py`
3. Добавить `UpdateAccount` в `src/entrypoints/http/public/schemas/accounts.py`
4. Добавить экспорт в `src/entrypoints/http/public/schemas/__init__.py`
5. `src/entrypoints/http/public/routers/accounts/update.py`
6. Добавить import и include в `registry.py`
