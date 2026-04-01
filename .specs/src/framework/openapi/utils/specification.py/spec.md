# src/framework/openapi/utils/specification.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/framework/openapi/utils/specification.py`.

## Поведение

Модуль определяет Функции: `findrefs`, `errors`.

## Входы

- `openapi`
- `typing.Any] | list[dict[str`
- `typing.Any]]`
- `find`
- `replace`
- `args`

## Выходы

- `None`
- `dict[int | str, dict[str, typing.Any]]`

## Зависимости

- `typing`
- `src.framework.openapi.collections: SPECIFICATION_COMPONENTS_SCHEMAS_REF_KEY`
- `src.framework.openapi.collections: SPECIFICATION_COMPONENTS_SCHEMAS_REF_PATH`
- `src.framework.openapi.collections: SPECIFICATION_PATHS_RESPONSES_CONTENT`
- `src.framework.openapi.collections: SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON`
- `src.framework.openapi.collections: SPECIFICATION_PATHS_RESPONSES_CONTENT_APPLICATION_JSON_EXAMPLE`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
