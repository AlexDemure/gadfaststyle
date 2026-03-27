# Architecture: Domain Layer

## Что входит в слой

- `src/domain/models/`
- `src/domain/collections/exceptions/`

## Как писать доменные модели

- Каждая сущность хранится в отдельном файле.
- Модель наследуется от проектной `Base`.
- Поля и их типы описываются явно.
- Для создания новой сущности используй classmethod вроде `init(...)`, если это уже сделано у существующих моделей.

Пример:

```python
# path: src/domain/models/account.py
import datetime
import typing

from src.common.formats.utils import date

from .base import Base


class Account(Base):
    __encrypted__ = ["external_id"]

    id: int | None
    external_id: str
    created: datetime.datetime
    updated: datetime.datetime
    blocked: datetime.datetime | None
    authorization: datetime.datetime | None

    @classmethod
    def init(cls, external_id: str) -> typing.Self:
        created = updated = date.now()

        return cls(
            id=None,
            external_id=external_id,
            created=created,
            updated=updated,
            blocked=None,
            authorization=None,
        )
```

## Как писать доменные исключения

- Исключения домена лежат в отдельном файле сущности.
- Наследование идет от `HTTPError`, если это уже текущая форма проектных исключений.
- Имена исключений строятся от сущности и сценария.

Пример:

```python
# path: src/domain/collections/exceptions/account.py
from src.common.http.collections import HTTPError


class AccountNotFound(HTTPError): ...


class AccountBlocked(HTTPError): ...


class AccountAlreadyExists(HTTPError): ...
```

## Правила написания

- Если появляется новая сущность, создай новый файл модели и новый файл исключений по той же схеме.
- Не складывай несколько несвязанных сущностей в один файл.
- Не тащи инфраструктурные зависимости в домен.
- Если у модели есть специальные поля вроде `__encrypted__`, повторяй текущий проектный подход, а не придумывай новый.
