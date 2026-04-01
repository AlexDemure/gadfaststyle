# src/infrastructure/databases/orm/sqlalchemy/utils/execute.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/infrastructure/databases/orm/sqlalchemy/utils/execute.py`.

## Поведение

Модуль определяет Функции: `fetchcount`, `fetchone`, `fetchall`.

## Входы

- `session`
- `statement`

## Выходы

- `int`
- `Table`
- `list[Table]`

## Зависимости

- `typing`
- `sqlalchemy: func`
- `sqlalchemy: select`
- `sqlalchemy.exc: NoResultFound`
- `src.infrastructure.databases.orm.sqlalchemy.collections: ObjectNotFound`
- `src.infrastructure.databases.orm.sqlalchemy.session: Session`
- `src.infrastructure.databases.orm.sqlalchemy.tables: Table`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
