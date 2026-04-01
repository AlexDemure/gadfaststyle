# src/infrastructure/databases/orm/sqlalchemy/builders/filter.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать сборщики и конструкторы модуля `src/infrastructure/databases/orm/sqlalchemy/builders/filter.py`.

## Поведение

Модуль определяет Классы: `Builder`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `typing`
- `sqlalchemy: and_`
- `sqlalchemy: or_`
- `src.infrastructure.databases.orm.sqlalchemy.models: And`
- `src.infrastructure.databases.orm.sqlalchemy.models: Filter`
- `src.infrastructure.databases.orm.sqlalchemy.models: Or`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
