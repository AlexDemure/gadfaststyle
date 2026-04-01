# src/infrastructure/databases/postgres/adapters/repositories/base.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать базовые абстракции модуля `src/infrastructure/databases/postgres/adapters/repositories`.

## Поведение

Модуль определяет Классы: `Base`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `typing`
- `src.common.formats.utils: date`
- `src.common.typings.variables: Error`
- `src.domain.models: Model`
- `src.infrastructure.databases.orm.sqlalchemy.collections: ObjectNotFound`
- `src.infrastructure.databases.orm.sqlalchemy.crud: Crud`
- `src.infrastructure.databases.orm.sqlalchemy.models: And`
- `src.infrastructure.databases.orm.sqlalchemy.models: Filter`
- `src.infrastructure.databases.orm.sqlalchemy.models: Or`
- `src.infrastructure.databases.orm.sqlalchemy.models: Pagination`
- `src.infrastructure.databases.orm.sqlalchemy.models: Sorting`
- `src.infrastructure.databases.orm.sqlalchemy.session: Session`
- `src.infrastructure.databases.orm.sqlalchemy.tables: Table`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
