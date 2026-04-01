# src/infrastructure/databases/orm/sqlalchemy/models/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `models`.

## Поведение

Файл собирает и экспортирует: `And`, `Filter`, `Function`, `Or`, `Pagination`, `Sorting`.

## Входы

- Импортируемые объекты пакета: `And`, `Filter`, `Function`, `Or`, `Pagination`, `Sorting`

## Выходы

- Публичный импорт `And`
- Публичный импорт `Filter`
- Публичный импорт `Function`
- Публичный импорт `Or`
- Публичный импорт `Pagination`
- Публичный импорт `Sorting`

## Зависимости

- `statement: And`
- `statement: Filter`
- `statement: Function`
- `statement: Or`
- `statement: Pagination`
- `statement: Sorting`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
