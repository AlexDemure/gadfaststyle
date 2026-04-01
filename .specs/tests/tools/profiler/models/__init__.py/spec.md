# tests/tools/profiler/models/__init__.py

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

Файл собирает и экспортирует: `Allocation`, `GarbageCollector`, `PostgresExplain`, `SqlalchemyProfiling`, `SqlalchemyQuery`, `Statistics`.

## Входы

- Импортируемые объекты пакета: `Allocation`, `GarbageCollector`, `PostgresExplain`, `SqlalchemyProfiling`, `SqlalchemyQuery`, `Statistics`

## Выходы

- Публичный импорт `Allocation`
- Публичный импорт `GarbageCollector`
- Публичный импорт `PostgresExplain`
- Публичный импорт `SqlalchemyProfiling`
- Публичный импорт `SqlalchemyQuery`
- Публичный импорт `Statistics`

## Зависимости

- `profilers: SqlalchemyProfiling`
- `reports: Allocation`
- `reports: GarbageCollector`
- `reports: PostgresExplain`
- `reports: SqlalchemyQuery`
- `reports: Statistics`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
