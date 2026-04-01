## Описание

`postgres/collections` описывает коллекции Postgres-слоя.

## Правила

- В `collections` держи Postgres-константы и исключения.
- Не смешивай их с CRUD, adapters и tables.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.databases.postgres.collections import exceptions
```
