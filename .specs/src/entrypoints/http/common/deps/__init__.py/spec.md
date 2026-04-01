# src/entrypoints/http/common/deps/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `deps`.

## Поведение

Файл собирает и экспортирует: `basic`, `jwt`.

## Входы

- Импортируемые объекты пакета: `basic`, `jwt`

## Выходы

- Публичный импорт `basic`
- Публичный импорт `jwt`

## Зависимости

- `security: basic`
- `security: jwt`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
