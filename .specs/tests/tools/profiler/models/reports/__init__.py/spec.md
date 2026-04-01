# tests/tools/profiler/models/reports/__init__.py

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

Файл собирает и экспортирует: `Allocation`, `GarbageCollector`, `PostgresExplain`, `SqlalchemyQuery`, `Statistics`.

## Входы

- Импортируемые объекты пакета: `Allocation`, `GarbageCollector`, `PostgresExplain`, `SqlalchemyQuery`, `Statistics`

## Выходы

- Публичный импорт `Allocation`
- Публичный импорт `GarbageCollector`
- Публичный импорт `PostgresExplain`
- Публичный импорт `SqlalchemyQuery`
- Публичный импорт `Statistics`

## Зависимости

- `extensions: PostgresExplain`
- `extensions: SqlalchemyQuery`
- `python: Allocation`
- `python: GarbageCollector`
- `python: Statistics`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
