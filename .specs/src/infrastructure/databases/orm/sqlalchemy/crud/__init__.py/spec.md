# src/infrastructure/databases/orm/sqlalchemy/crud/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `crud`.

## Поведение

Файл собирает и экспортирует: `Base`, `Crud`.

## Входы

- Импортируемые объекты пакета: `Base`, `Crud`

## Выходы

- Публичный импорт `Base`
- Публичный импорт `Crud`

## Зависимости

- `base: Base`
- `base: Crud`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
