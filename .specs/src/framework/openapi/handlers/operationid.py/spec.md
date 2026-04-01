# src/framework/openapi/handlers/operationid.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/framework/openapi/handlers/operationid.py`.

## Поведение

Модуль определяет Функции: `handler`.

## Входы

- `app`
- `openapi`
- `typing.Any]`
- `exclude`

## Выходы

- `tuple[FastAPI, dict[str, typing.Any]]`

## Зависимости

- `collections.abc`
- `typing`
- `collections: Counter`
- `fastapi: FastAPI`
- `src.common.formats.utils: string`
- `src.framework.openapi.collections: FASTAPI_ROUTE_PATH`
- `src.framework.openapi.collections: SPECIFICATION_ENDPOINT`
- `src.framework.openapi.collections: SPECIFICATION_OPERATION_ID`
- `src.framework.openapi.collections: SPECIFICATION_PATHS`
- `src.framework.openapi.collections: SPECIFICATION_ROUTES`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
