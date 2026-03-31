## Описание

`postgres` описывает Postgres-реализацию database-инфраструктуры.

## Правила

- Новая сущность проходит через `tables`, `crud`, `adapters`.
- SQLAlchemy table, CRUD и repository adapter держи в разных слоях.
- Runtime-код не смешивай с миграциями.
- Миграции создавай отдельно через Alembic.

## Примеры

```python
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables
```
