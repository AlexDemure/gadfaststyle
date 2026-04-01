# src/infrastructure/databases/orm/sqlalchemy/queries/statement.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать запросы и утилиты выборки модуля `src/infrastructure/databases/orm/sqlalchemy/queries/statement.py`.

## Поведение

Модуль определяет Классы: `JSONBArray`, `Array`, `Range`, `Search`, `Comparison`, `Filter`, `Pagination`, `Sorting`, `And`, `Or`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `typing`
- `sqlalchemy: func`
- `src.infrastructure.databases.orm.sqlalchemy: models`
- `src.infrastructure.databases.orm.sqlalchemy.collections: Direction`
- `src.infrastructure.databases.orm.sqlalchemy.collections: Operator`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
