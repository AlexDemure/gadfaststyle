# src/infrastructure/databases/postgres/crud/account.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Описать CRUD-модуль `account`.

## Поведение

Модуль определяет классы: `Account`. Модуль инкапсулирует операции чтения и записи для persistence-слоя.

## Входы

- Внутренние зависимости текущего слоя

## Выходы

- Классы `Account`

## Зависимости

- `src.infrastructure.databases.orm.sqlalchemy.crud: Base`
- `src.infrastructure.databases.postgres: tables`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
