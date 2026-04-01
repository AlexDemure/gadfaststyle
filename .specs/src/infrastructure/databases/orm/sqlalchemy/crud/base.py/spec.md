# src/infrastructure/databases/orm/sqlalchemy/crud/base.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать базовые абстракции модуля `src/infrastructure/databases/orm/sqlalchemy/crud`.

## Поведение

Модуль определяет Классы: `Base`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `typing`
- `sqlalchemy: Select`
- `sqlalchemy: bindparam`
- `sqlalchemy: delete`
- `sqlalchemy: exists`
- `sqlalchemy: select`
- `sqlalchemy: text`
- `sqlalchemy: update`
- `src.infrastructure.databases.orm.sqlalchemy: builders`
- `src.infrastructure.databases.orm.sqlalchemy: models`
- `src.infrastructure.databases.orm.sqlalchemy: tables`
- `src.infrastructure.databases.orm.sqlalchemy.session: Session`
- `src.infrastructure.databases.orm.sqlalchemy.utils: fetchall`
- `src.infrastructure.databases.orm.sqlalchemy.utils: fetchcount`
- `src.infrastructure.databases.orm.sqlalchemy.utils: fetchone`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
