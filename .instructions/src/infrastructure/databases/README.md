## Описание

`databases` описывает database-инфраструктуру.

## Правила

- Runtime и клиенты баз данных держи в `databases/`.
- Конкретную реализацию БД раскладывай по отдельному пакету, например `postgres/`.
- Таблицы, CRUD и adapters не смешивай в одном слое.

## Примеры

```python
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables
```
