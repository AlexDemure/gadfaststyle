# tests/tools/profiler/reports/extensions/sqlalchemy.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать отчеты модуля `tests/tools/profiler/reports/extensions/sqlalchemy.py`.

## Поведение

Модуль определяет Функции: `generate`.

## Входы

- `sql`
- `Statistics`
- `Statistics]`
- `orm`
- `explains`

## Выходы

- `SqlalchemyQuery`

## Зависимости

- `tests.tools.profiler.models: PostgresExplain`
- `tests.tools.profiler.models: SqlalchemyQuery`
- `tests.tools.profiler.models: Statistics`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
