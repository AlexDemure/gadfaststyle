# Architecture: Application Layer

## Что входит в слой

- `src/application/usecases/`

## Как организован usecase

Usecase оформляется отдельным файлом операции внутри доменной папки:

- `src/application/usecases/<domain>/create.py`
- `src/application/usecases/<domain>/delete.py`
- `src/application/usecases/<domain>/get/...`

Если у домена появляется несколько сценариев, держи их рядом в отдельной папке домена.

## Базовая форма usecase

- Используются классы `Repository`, `Security`, `Container`, `Usecase`.
- `Usecase` хранит `self.container`.
- Инициализация зависимостей происходит в `build(session)`.
- Сам вызов идет через `async def __call__(...)`.
- Для БД-сценариев используется `@sessionmaker.write` или соответствующий декоратор текущего паттерна.

Эталон:

```python
# path: src/application/usecases/accounts/create.py
from src.decorators import sessionmaker
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.models import Tokens


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption
        self.jwt = jwt


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
    async def __call__(self, session: Session, external_id: str) -> Tokens:
        self.build(session)

        if await self.container.repository.account.exists(
            Filter.eq(
                key="external_id",
                value=self.container.security.encryption.encrypt(external_id.lower()),
            )
        ):
            raise AccountAlreadyExists

        account = await self.container.repository.account.create(
            model=Account.init(
                **Account.encrypt(
                    encrypter=self.container.security.encryption.encrypt,
                    external_id=external_id,
                ),
            )
        )

        tokens = self.container.security.jwt.encode(subject=str(account.id))

        return tokens
```

## Правила написания

- Сначала смотри соседний usecase того же домена и копируй его форму.
- Если в модуле уже используется `Repository`, не вводи рядом `Repositories`.
- В usecase допускается orchestration: проверки, вызовы репозиториев, security, сборка ответа.
- Доменные ошибки поднимай через `src.domain.collections`.
- Не переноси HTTP-детали в usecase.

## Именование

- Файл называется по операции.
- Класс сценария всегда `Usecase`.
- Контейнер зависимостей называется `Container`.
- Агрегатор репозиториев называется так же, как сделано рядом: `Repository` или другой уже существующий вариант соседнего модуля.

## Что запрещено

- Не обращаться к таблицам напрямую из usecase.
- Не строить raw SQL в usecase.
- Не создавать новый стиль DI, если текущий домен уже задает паттерн.
