## Описание

`postgres/migrations` описывает миграционный каркас Postgres.

## Правила

- В `migrations` держи только Alembic-каркас и миграционные файлы.
- Runtime-код приложения не размещай здесь.
- Миграции должны быть согласованы с `tables/`.

## Примеры

```text
src/infrastructure/databases/postgres/migrations/
```
