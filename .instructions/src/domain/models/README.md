## Описание

`models` описывает доменные модели.

## Правила

- Каждая сущность лежит в отдельном файле.
- Модель наследуется от принятой domain `Base`.
- Поля и их типы описывай явно.
- Для создания новой сущности используй `init(...)` или уже принятый factory-паттерн.
- Публичные модели экспортируй через `models/__init__.py`, чтобы код писал `from src.domain.models import Account`.

## Примеры

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

    @classmethod
    def init(cls, external_id: str) -> typing.Self:
        created = updated = date.now()

        return cls(
            id=None,
            external_id=external_id,
            created=created,
            updated=updated,
        )
```
