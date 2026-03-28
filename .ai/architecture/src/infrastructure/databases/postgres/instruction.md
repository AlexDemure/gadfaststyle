# Infrastructure Databases: Postgres

## Что входит в раздел

- `src/infrastructure/databases/postgres/tables/`
- `src/infrastructure/databases/postgres/crud/`
- `src/infrastructure/databases/postgres/adapters/repositories/`
- `src/infrastructure/databases/postgres/migrations/`

## Базовая цепочка новой сущности

Новая сущность в Postgres обычно проходит три слоя:

1. `tables/<entity>.py`
2. `crud/<entity>.py`
3. `adapters/repositories/<entity>.py`

## Навигация

- Детали по таблицам: `.ai/architecture/src/infrastructure/databases/postgres/tables/instruction.md`
- Детали по CRUD: `.ai/architecture/src/infrastructure/databases/postgres/crud/instruction.md`
- Детали по adapter-слою: `.ai/architecture/src/infrastructure/databases/postgres/adapters/instruction.md`

## Базовые правила

- Если появляется новая сущность, создавай все три уровня, а не пропускай adapter.
- SQLAlchemy table, CRUD и repository adapter должны оставаться разнесенными по своим слоям.
- Миграции оформляй отдельно и не смешивай с runtime-кодом.
