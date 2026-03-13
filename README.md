<p align="center">
  <a href="https://github.com/AlexDemure/gadfaststyle">
    <a href="https://ibb.co/TqkGRPCN"><img src="https://i.ibb.co/sJ24QsBX/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  File architecture for FastApi app
</p>

---

# О проекте

`gadfaststyle` — проект на `FastAPI` с модульной структурой backend-приложения.

Репозиторий содержит базовые инфраструктурные компоненты и интеграции, используемые при разработке API-сервисов и фоновых процессов.

На текущем этапе в приложение уже интегрированы:

- Модуль `Basic Auth` для защиты служебных и административных эндпоинтов.
- Подсистема шифрования для безопасной обработки чувствительных данных.
- `PostgreSQL` как основное транзакционное хранилище данных.
- `SQLAlchemy` как ORM-слой для работы с моделями и запросами к базе данных.
- `Alembic` для контроля версий схемы и управления миграциями базы данных.
- `APScheduler` для выполнения фоновых и регулярных задач по расписанию.
- `Telegram Bot`-контур для интеграции с пользовательскими и операционными сценариями.
- `Jinja2` для шаблонизации и генерации динамического контента.
- Централизованный модуль логгирования для мониторинга и диагностики.
- Интеграция с `Sentry` для трекинга ошибок и анализа сбоев.
- `Redis` для кэширования и вспомогательных runtime-механизмов.
- `JWT-аутентификация` для управления пользовательскими сессиями и токенами доступа.

# Использование

Ниже показана цепочка прохождения данных для эндпоинта `entrypoints.http.public.accounts.create` без полной реализации деталей.

```python
# schemas -> deps -> endpoint -> usecase -> adapter -> crud -> table

# =========================
# SCHEMAS
# file: src/entrypoints/http/public/schemas/accounts.py
# =========================
from src.entrypoints.http.common.schemas import Command, Request
from src.entrypoints.http.public.schemas.base import Public


class CreateAccount(Public, Request, Command):
    external_id: str


# =========================
# DEPS
# file: src/entrypoints/http/public/deps/accounts/create.py
# =========================
from fastapi import Depends
from src.application.usecases.accounts.create import Container, Repositories, Security, Usecase
from src.entrypoints.http.common.deps import write
from src.infrastructure.databases.orm.sqlalchemy.session import Session


def dependency(session: Session = Depends(write)) -> Usecase:
    return Usecase(container=Container(repositories=Repositories(session), security=Security()))


# =========================
# ENDPOINT
# file: src/entrypoints/http/public/routers/accounts/create.py
# =========================
from fastapi import Body, Depends
from src.entrypoints.http.public.schemas import CreateAccount
from src.framework.routing import APIRouter
from src.infrastructure.security.jwt.models import Tokens

router = APIRouter()


@router.post("/accounts:create")
async def command(
    usecase: Usecase = Depends(dependency),
    body: CreateAccount = Body(...),
) -> Tokens:
    return await usecase(**body.deserialize())


# =========================
# USECASE
# file: src/application/usecases/accounts/create.py
# =========================
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt


class Repositories:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption
        self.jwt = jwt


class Container:
    def __init__(self, repositories: Repositories, security: Security) -> None:
        self.repositories = repositories
        self.security = security


class Usecase:
    def __init__(self, container: Container) -> None:
        self.container = container

    async def __call__(self, external_id: str) -> Tokens:
        exists = await self.container.repositories.account.exists(
            Filter.eq(
                key="external_id",
                value=self.container.security.encryption.encrypt(external_id.lower()),
            )
        )
        if exists:
            raise AccountAlreadyExists

        account = await self.container.repositories.account.create(
            model=Account.init(
                **Account.encrypt(
                    encrypter=self.container.security.encryption.encrypt,
                    external_id=external_id,
                )
            )
        )
        return self.container.security.jwt.encode(subject=str(account.id))


# =========================
# DOMAIN MODEL
# file: src/domain/models/account.py
# =========================
import datetime

from src.common.formats.utils import date
from src.domain.models.base import Base


class Account(Base):
    __encrypted__ = ["external_id"]

    id: int | None
    external_id: str
    created: datetime.datetime
    updated: datetime.datetime
    blocked: datetime.datetime | None
    authorization: datetime.datetime | None

    @classmethod
    def init(cls, external_id: str) -> "Account":
        created = updated = date.now()
        return cls(
            id=None,
            external_id=external_id,
            created=created,
            updated=updated,
            blocked=None,
            authorization=None,
        )


# =========================
# DOMAIN ERRORS
# file: src/domain/collections/exceptions/account.py
# =========================
from src.common.http.collections import HTTPError


class AccountNotFound(HTTPError): ...
class AccountBlocked(HTTPError): ...
class AccountAlreadyExists(HTTPError): ...


# =========================
# ADAPTER
# file: src/infrastructure/databases/postgres/adapters/repositories/account.py
# =========================
from src.infrastructure.databases.postgres import crud, tables


class Account:
    crud = crud.Account
    table = tables.Account

    # exists(...) -> delegating to crud.Account.exists(...)
    # create(...) -> delegating to crud.Account.create(...)


# =========================
# CRUD
# file: src/infrastructure/databases/postgres/crud/account.py
# =========================
from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.postgres import tables


class Account(Base[tables.Account]):
    table = tables.Account
    # Base.create(session, row) -> INSERT account ...
    # Base.exists(session, filters...) -> SELECT EXISTS(...)


# =========================
# TABLE
# file: src/infrastructure/databases/postgres/tables/account.py
# =========================
from sqlalchemy import BigInteger, Column, DateTime, String
from src.infrastructure.databases.orm.sqlalchemy.tables import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    external_id = Column(String, nullable=False, unique=True)
    created = Column(DateTime(timezone=True), nullable=False)
    updated = Column(DateTime(timezone=True), nullable=False)
    blocked = Column(DateTime(timezone=True), nullable=True)
    authorization = Column(DateTime(timezone=True), nullable=True)
```

# Развертывание module.toml

Пример генерации модуля по шаблону `.templates/module.toml`:

```bash
uv add gadcodegenerator

# Add module
uv run gadcodegenerator -f https://raw.githubusercontent.com/AlexDemure/gadfaststyle/refs/heads/main/.templates/module.toml --context '{"module": {"snake": {"single": "user", "many": "users"}, "pascal": {"single": "User", "many": "Users"}, "kebab": {"single": "user", "many": "users"}}}'
```

# Дерево папок проекта

```text
.
├── .ai
│   ├── agents
│   │   ├── _templates
│   │   └── code-writer
│   └── rules
├── .compose
├── .scripts
│   └── lints
│       └── configs
├── .templates
├── src
│   ├── application
│   │   ├── usecases
│   │   │   └── accounts
│   │   │       └── get
│   │   └── utils
│   ├── bootstrap
│   ├── common
│   │   ├── calendar
│   │   ├── formats
│   │   ├── http
│   │   ├── human
│   │   ├── keyboard
│   │   ├── locales
│   │   ├── os
│   │   ├── socials
│   │   └── typings
│   ├── configuration
│   ├── domain
│   │   ├── collections
│   │   │   ├── enums
│   │   │   └── exceptions
│   │   └── models
│   ├── entrypoints
│   │   ├── cron
│   │   ├── http
│   │   │   ├── common
│   │   │   ├── public
│   │   │   └── system
│   │   └── workers
│   │       └── telegram
│   │           └── aiogram
│   ├── framework
│   │   ├── background
│   │   ├── collections
│   │   ├── openapi
│   │   └── routing
│   ├── infrastructure
│   │   ├── databases
│   │   │   ├── orm
│   │   │   │   └── sqlalchemy
│   │   │   └── postgres
│   │   │       ├── adapters
│   │   │       ├── collections
│   │   │       ├── crud
│   │   │       ├── migrations
│   │   │       │   └── versions
│   │   │       └── tables
│   │   ├── integrations
│   │   │   └── telegram
│   │   │       └── telethon
│   │   ├── monitoring
│   │   │   ├── asyncio
│   │   │   ├── health
│   │   │   ├── logging
│   │   │   └── sentry
│   │   ├── scheduling
│   │   │   └── apscheduler
│   │   ├── security
│   │   │   ├── encryption
│   │   │   └── jwt
│   │   └── storages
│   │       └── redis
│   ├── localization
│   │   └── models
│   ├── representation
│   └── static
│       └── localizations
└── tests
    ├── factories
    ├── mocking
    ├── test_integrations
    ├── test_loads
    ├── test_units
    └── tools
```
