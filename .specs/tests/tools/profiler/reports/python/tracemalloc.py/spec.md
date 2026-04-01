# tests/tools/profiler/reports/python/tracemalloc.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать отчеты модуля `tests/tools/profiler/reports/python/tracemalloc.py`.

## Поведение

Модуль определяет Функции: `generate`.

## Входы

- Прямые входы определяются вызывающим кодом модуля.

## Выходы

- `Allocation`

## Зависимости

- `tracemalloc`
- `tests.tools.profiler.models: Allocation`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
