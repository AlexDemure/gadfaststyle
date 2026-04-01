# tests/tools/profiler/reports/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `reports`.

## Поведение

Файл собирает и экспортирует: `garbage`, `postgres`, `sqlalchemy`, `statistics`, `tracemalloc`.

## Входы

- Импортируемые объекты пакета: `garbage`, `postgres`, `sqlalchemy`, `statistics`, `tracemalloc`

## Выходы

- Публичный импорт `garbage`
- Публичный импорт `postgres`
- Публичный импорт `sqlalchemy`
- Публичный импорт `statistics`
- Публичный импорт `tracemalloc`

## Зависимости

- `extensions: postgres`
- `extensions: sqlalchemy`
- `python: garbage`
- `python: statistics`
- `python: tracemalloc`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
