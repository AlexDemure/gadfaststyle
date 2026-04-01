# src/infrastructure/databases/postgres/tables/account.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Описать таблицу `account`.

## Поведение

Модуль определяет классы: `Account`. Модуль описывает ORM-модель и привязку полей к таблице БД.

## Входы

- Внутренние зависимости текущего слоя

## Выходы

- Классы `Account`

## Зависимости

- `sqlalchemy: BigInteger`
- `sqlalchemy: Column`
- `sqlalchemy: DateTime`
- `sqlalchemy: String`
- `src.infrastructure.databases.orm.sqlalchemy.tables: Base`
- `src.infrastructure.databases.postgres.collections: LENGTH_SMALL_STR`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
