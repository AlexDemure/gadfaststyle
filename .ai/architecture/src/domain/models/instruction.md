# Domain: Models

## Что входит в раздел

- `src/domain/models/`

## Базовые правила

- Каждая сущность хранится в отдельном файле.
- Модель наследуется от проектной `Base`.
- Поля и их типы описываются явно.
- Для создания новой сущности используй `classmethod` вроде `init(...)`, если это уже сделано у существующих моделей.
- Если у модели есть специальные поля вроде `__encrypted__`, повторяй текущий проектный подход.

## Что не делать

- Не складывай несколько несвязанных сущностей в один файл.
- Не тащи инфраструктурные зависимости в доменную модель.
- Не переноси в модель HTTP-логику или детали persistence-слоя.

## Эталон

```python
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
