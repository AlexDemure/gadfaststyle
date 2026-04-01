# tests/factories/infrastructure/databases/postgres/tables/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `tables`.

## Поведение

Файл собирает и экспортирует: `Table`.

## Входы

- Импортируемые объекты пакета: `Table`

## Выходы

- Публичный импорт `Table`

## Зависимости

- `base: Table`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
