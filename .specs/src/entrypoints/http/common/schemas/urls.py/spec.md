# src/entrypoints/http/common/schemas/urls.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать схемы и контракт данных модуля `src/entrypoints/http/common/schemas/urls.py`.

## Поведение

Модуль определяет Классы: `URL`, `Photo`.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `pydantic: BaseModel`
- `pydantic: field_validator`
- `src.common.formats.utils: urls`
- `src.common.typings.validators: Link`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
