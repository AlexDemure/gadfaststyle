# tests/tools/profiler/profilers/extensions/sqlaclhemy.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать профилировщик модуля `tests/tools/profiler/profilers/extensions/sqlaclhemy.py`.

## Поведение

Модуль определяет Классы: `SqlalchemyProfiler`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `asyncio`
- `typing`
- `sqlalchemy.dialects.postgresql: dialect`
- `sqlalchemy.ext.asyncio: AsyncSession`
- `sqlalchemy.sql: Executable`
- `sqlalchemy.sql: text`
- `tests.tools.profiler: contextmanagers`
- `tests.tools.profiler: models`
- `tests.tools.profiler: reports`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
