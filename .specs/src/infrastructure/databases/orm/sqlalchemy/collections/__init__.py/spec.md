# src/infrastructure/databases/orm/sqlalchemy/collections/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `collections`.

## Поведение

Файл собирает и экспортирует: `ClientDisabled`, `Direction`, `Isolation`, `ObjectNotFound`, `Operator`.

## Входы

- Импортируемые объекты пакета: `ClientDisabled`, `Direction`, `Isolation`, `ObjectNotFound`, `Operator`

## Выходы

- Публичный импорт `ClientDisabled`
- Публичный импорт `Direction`
- Публичный импорт `Isolation`
- Публичный импорт `ObjectNotFound`
- Публичный импорт `Operator`

## Зависимости

- `enums: Direction`
- `enums: Isolation`
- `enums: Operator`
- `exceptions: ClientDisabled`
- `exceptions: ObjectNotFound`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
