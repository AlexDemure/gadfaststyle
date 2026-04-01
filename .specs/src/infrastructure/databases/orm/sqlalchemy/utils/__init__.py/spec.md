# src/infrastructure/databases/orm/sqlalchemy/utils/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `utils`.

## Поведение

Файл собирает и экспортирует: `fetchall`, `fetchcount`, `fetchone`.

## Входы

- Импортируемые объекты пакета: `fetchall`, `fetchcount`, `fetchone`

## Выходы

- Публичный импорт `fetchall`
- Публичный импорт `fetchcount`
- Публичный импорт `fetchone`

## Зависимости

- `execute: fetchall`
- `execute: fetchcount`
- `execute: fetchone`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
