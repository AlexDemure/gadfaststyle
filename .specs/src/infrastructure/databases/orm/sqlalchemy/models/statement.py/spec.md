# src/infrastructure/databases/orm/sqlalchemy/models/statement.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать модели модуля `src/infrastructure/databases/orm/sqlalchemy/models/statement.py`.

## Поведение

Модуль определяет Классы: `Sorting`, `Pagination`, `Filter`, `And`, `Or`, `Function`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `typing`
- `pydantic: BaseModel`
- `sqlalchemy.sql.visitors: Visitable`
- `src.infrastructure.databases.orm.sqlalchemy.collections: Direction`
- `src.infrastructure.databases.orm.sqlalchemy.collections: Operator`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
