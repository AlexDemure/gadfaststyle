# src/common/formats/utils/json.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/common/formats/utils/json.py`.

## Поведение

Модуль определяет Функции: `tostring`, `fromstring`, `atob`.

## Входы

- `obj`
- `sort_keys`
- `indent`
- `ensure_ascii`
- `text`

## Выходы

- `str`
- `typing.Any`

## Зависимости

- `base64`
- `json`
- `typing`
- `src.common.formats.encoders: JSONEncoder`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
