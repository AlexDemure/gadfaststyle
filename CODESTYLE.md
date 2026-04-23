# Инструменты

- Линтинг: `.scripts/lints/run.py`
- Порядок: `isort` -> `ruff check --fix` -> `ruff format` -> `mypy`
- Конфиги: `.scripts/lints/configs/`

# Quick Rules

- Все функции аннотированы.
- Один импорт = одна строка.
- Кавычки — двойные.
- Длина строки — 120.
- Отступ — 4 пробела.
- Используй `|` вместо `typing.Union`.
- Используй `typing.Self` там, где класс возвращает себя.
- Не делай parent-relative imports.

# Импорты

Порядок групп:

1. stdlib
2. third-party
3. `src.*`
4. `tests.*`

Правила:

- Между группами одна пустая строка.
- После блока импортов две пустые строки.
- Если пакет экспортирует объект через `__init__.py`, импортируй из пакета.

Верно:

```python
import datetime
import typing

from fastapi import Depends

from src.domain.models import Account
```

Неверно:

```python
from datetime import datetime, timedelta
from ..crud import account
```

# Именование

- классы: `PascalCase`
- функции и методы: `snake_case`
- переменные: `snake_case`
- константы: `UPPER_SNAKE_CASE`
- модули: `snake_case`

Зафиксированные имена:

- usecase-класс: `Usecase`
- dependency factory: `dependency`
- command handler: `command`
- query handler: `query`
- base-класс: `Base`

Структурные правила:

- один публичный класс на файл;
- имя файла соответствует операции или роли (`create.py`, `current.py`, `base.py`).

# Типизация

- Нет неаннотированных функций.
- Нет `Any` без необходимости.
- Generics всегда с параметром типа.

Верно:

```python
self.container: types.SimpleNamespace | None = None
items: list[str]

@classmethod
def init(cls, external_id: str) -> typing.Self: ...
```

# Форматирование

- Длинные вызовы разбивай вертикально.
- Предпочитай trailing comma.

```python
return cls(
    id=None,
    external_id=external_id,
    created=created,
    updated=updated,
)
```

# `collections/`

Структура:

```text
collections/
├── const/
├── enums/
└── exceptions/
```

Экспортируй через `__init__.py`:

```python
from .exceptions.account import AccountNotFound

__all__ = [
    "AccountNotFound",
]
```

# Domain Models

- Все доменные модели наследуются от `Base`.
- Для зашифрованных моделей используй `__encrypted__`.
- `init(...)` должен содержать бизнес-конструирование объекта.
- `encrypt`/`decrypt` вызывай через методы модели, не напрямую из usecase.

# Exceptions

- Доменные исключения наследуются от `HTTPError`.
- `code` задаётся через `HTTPCode`.
- Поднимай без аргументов: `raise AccountNotFound`.
- При перехвате используй chaining: `raise TokenInvalid from error`.
