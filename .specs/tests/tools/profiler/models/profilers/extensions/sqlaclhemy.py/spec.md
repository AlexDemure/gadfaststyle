# tests/tools/profiler/models/profilers/extensions/sqlaclhemy.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать модели модуля `tests/tools/profiler/models/profilers/extensions/sqlaclhemy.py`.

## Поведение

Модуль определяет Классы: `SqlalchemyProfiling`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `pydantic: BaseModel`
- `tests.tools.profiler.models.reports.extensions.sqlalchemy: SqlalchemyQuery`
- `tests.tools.profiler.models.reports.python.garbage: GarbageCollector`
- `tests.tools.profiler.models.reports.python.tracemalloc: Allocation`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
