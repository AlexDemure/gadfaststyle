# tests/tools/profiler/contextmanagers/tracemalloc.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать контекстный менеджер модуля `tests/tools/profiler/contextmanagers/tracemalloc.py`.

## Поведение

Модуль определяет Функции: `allocation`.

## Входы

- Прямые входы определяются вызывающим кодом модуля.

## Выходы

- `typing.Generator[None]`

## Зависимости

- `contextlib`
- `tracemalloc`
- `typing`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
