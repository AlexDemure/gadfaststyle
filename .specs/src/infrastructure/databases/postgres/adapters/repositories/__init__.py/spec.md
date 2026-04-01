# src/infrastructure/databases/postgres/adapters/repositories/__init__.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `repositories`.

## Поведение

Файл собирает и экспортирует: `Account`, `Base`.

## Входы

- Импортируемые объекты пакета: `Account`, `Base`

## Выходы

- Публичный импорт `Account`
- Публичный импорт `Base`

## Зависимости

- `account: Account`
- `base: Base`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
