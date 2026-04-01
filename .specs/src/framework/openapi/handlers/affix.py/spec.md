# src/framework/openapi/handlers/affix.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/framework/openapi/handlers/affix.py`.

## Поведение

Модуль определяет Функции: `handler`.

## Входы

- `app`
- `openapi`
- `typing.Any]`

## Выходы

- `tuple[FastAPI, dict[str, typing.Any]]`

## Зависимости

- `typing`
- `fastapi: FastAPI`
- `src.framework.openapi.collections: SPECIFICATION_COMPONENTS`
- `src.framework.openapi.collections: SPECIFICATION_COMPONENTS_SCHEMAS`
- `src.framework.openapi.collections: SPECIFICATION_COMPONENTS_SCHEMAS_TITLE`
- `src.framework.openapi.utils: findrefs`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
