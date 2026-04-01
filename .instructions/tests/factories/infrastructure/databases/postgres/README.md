## Описание

`factories/infrastructure/databases/postgres` описывает Postgres-фабрики для тестов.

## Правила

- Здесь создавай table-объекты и данные слоя хранения Postgres-слоя.
- Фабрики должны быть согласованы с `src.infrastructure.databases.postgres.tables`.
- Не смешивай их с HTTP и domain-фикстурами.

## Примеры

```python
from tests.factories.infrastructure.databases.postgres import tables
```
