## Правила

- Новая сущность в Postgres проходит через `tables`, `crud`, `adapters`.
- SQLAlchemy table, CRUD и repository adapter держи в разных слоях.
- Агент не пишет миграции вместе с runtime-кодом.
- Миграции создаются отдельно через Alembic.
