# Architecture: Infrastructure Layer

## Что входит в слой

- `src/infrastructure/databases/`
- `src/infrastructure/security/`
- `src/infrastructure/storages/`
- `src/infrastructure/monitoring/`
- `src/configuration/setup.py`
- `src/bootstrap/server.py`

## База данных: table, crud, adapter

Новая сущность в Postgres обычно проходит три слоя:

1. `tables/<entity>.py`
2. `crud/<entity>.py`
3. `adapters/repositories/<entity>.py`

### Table

```python
# path: src/infrastructure/databases/postgres/tables/account.py
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from src.infrastructure.databases.orm.sqlalchemy.tables import Base
from src.infrastructure.databases.postgres.collections import LENGTH_SMALL_STR


class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)

    external_id = Column(String(length=LENGTH_SMALL_STR), nullable=False, unique=True)

    created = Column(DateTime(timezone=True), nullable=False)
    updated = Column(DateTime(timezone=True), nullable=False)
    blocked = Column(DateTime(timezone=True), nullable=True)
    authorization = Column(DateTime(timezone=True), nullable=True)
```

### Crud

```python
# path: src/infrastructure/databases/postgres/crud/account.py
from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.postgres import tables


class Account(Base[tables.Account]):
    table = tables.Account
```

### Repository adapter

```python
# path: src/infrastructure/databases/postgres/adapters/repositories/account.py
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
```

## Правила для инфраструктуры БД

- Если появляется новая сущность, создавай все три уровня, а не пропускай adapter.
- Имена файлов и классов повторяют имя сущности: `account.py` -> `Account`.
- Usecase работает с adapter/repository, не с CRUD напрямую, если домен уже следует этой форме.
- Если нужна миграция, она идет отдельно в `src/infrastructure/databases/postgres/migrations/versions/`.

## Как писать инфраструктурный клиент

Новый клиент должен иметь lifecycle и singleton setup.

Пример клиента:

```python
# path: src/infrastructure/storages/redis/client.py
class Redis:
    def __init__(self) -> None:
        self.client: redis.Redis | None = None
        self.router = APIRouter(tags=["Cache"])
        self.endpoints()

    async def start(self) -> None:
        if not settings.REDIS:
            return

        self.client = redis.from_url(settings.REDIS_HOST, encoding="utf8", decode_responses=True)

        await self.client.ping()  # type:ignore

    async def shutdown(self) -> None:
        if not self.client:
            return

        await self.client.close()
```

Пример setup singleton:

```python
# path: src/infrastructure/storages/redis/setup.py
from .client import Redis


redis = Redis()
```

## Обязательные правила для нового клиента

- Клиент должен иметь `start()` и `shutdown()`, если он управляет внешним соединением.
- Инстанс создается в `setup.py`.
- Публичный singleton импортируется через `__init__.py`, если слой уже использует такой способ.
- Подключение клиента должно быть добавлено в `src/bootstrap/server.py`.
- Конфигурация клиента должна быть добавлена в `src/configuration/setup.py`.
- Значения должны читаться из `.env` через `BaseSettings`, а не через разрозненные `os.getenv`.

## Как подключать в settings

Пример формы:

```python
# path: src/configuration/setup.py
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Redis(BaseSettings):
    REDIS: bool = False
    REDIS_HOST: str | None = None


configs = [
    Redis,
]


class Settings(*configs):  # type:ignore
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
```

## Как подключать в bootstrap

Пример формы lifecycle:

```python
# path: src/bootstrap/server.py
@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> typing.Any:
    postgres.start()
    await redis.start()
    detector.start()
    background.start()
    logger.info("Application started")
    yield
    logger.info("Application shutdown")
    background.shutdown()
    detector.shutdown()
    await redis.shutdown()
    postgres.shutdown()
```

## Что важно по стилю

- Не подключай клиент неявно; lifecycle должен быть виден в `bootstrap/server.py`.
- Не храни настройки клиента в самом клиенте, если они уже живут в `settings`.
- Не придумывай другой стиль singleton-подключения, если рядом уже есть `setup.py`.
- Импорты и имена классов держи в том же стиле, что у `postgres`, `redis`, `jwt`, `encryption`.
