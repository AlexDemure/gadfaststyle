## Описание

`sqlalchemy/collections` описывает коллекции ORM-слоя.

## Правила

- В `collections` держи только enum, исключения и константы ORM-слоя.
- Не смешивай коллекции с builders и query-утилитами.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy.collections import exceptions
```
