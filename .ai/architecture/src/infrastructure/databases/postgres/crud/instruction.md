# Infrastructure Databases Postgres: Crud

## Что входит в раздел

- `src/infrastructure/databases/postgres/crud/`

## Базовые правила

- Для каждой сущности создавай отдельный CRUD-класс.
- CRUD связывает generic-базу с конкретной SQLAlchemy table.
- Для бизнес-ручек `:search` добавляй отдельный entity-specific метод `search(...)`.
- В `search(...)` собирай SQLAlchemy `statement` вручную под конкретную бизнес-ручку, а не через generic `paginated(...)`.
- `paginated(...)` оставляй для простых ручек `:paginated`, когда нужен пакетный доступ к данным без сложной логики выборки.
- Не смешивай CRUD с adapter-логикой и доменными моделями.

## Эталон

```python
from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.postgres import tables


class Account(Base[tables.Account]):
    table = tables.Account
```
