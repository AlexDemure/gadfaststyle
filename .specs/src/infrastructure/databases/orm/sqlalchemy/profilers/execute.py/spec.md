# src/infrastructure/databases/orm/sqlalchemy/profilers/execute.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать профилировщик модуля `src/infrastructure/databases/orm/sqlalchemy/profilers/execute.py`.

## Поведение

Модуль определяет Функции: `profiler`.

## Входы

- `session`

## Выходы

- `None`

## Зависимости

- `logging`
- `time`
- `typing`
- `sqlalchemy: Executable`
- `sqlalchemy: Result`
- `sqlalchemy.ext.asyncio: AsyncSession`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
