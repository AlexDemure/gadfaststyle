## Описание

`deps` описывает public dependencies.

## Правила

- DI-функция лежит рядом с доменом и операцией внутри `public`.
- Фабрику называй `dependency`.
- Если достаточно вернуть `Usecase()`, не добавляй лишнюю логику.
- Если пакет уже использует более сложную сборку зависимостей, повторяй локальный паттерн.

## Примеры

```python
from src.application.usecases.accounts.create import Usecase


def dependency() -> Usecase:
    return Usecase()
```
