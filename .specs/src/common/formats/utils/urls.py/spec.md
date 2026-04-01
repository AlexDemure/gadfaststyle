# src/common/formats/utils/urls.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/common/formats/utils/urls.py`.

## Поведение

Модуль определяет Функции: `parse`, `check`, `join`, `download`, `safe`, `allowed`, `normalize`, `equal`.

## Входы

- `url`
- `scheme`
- `domain`
- `path`
- `domains`
- `first`
- `second`

## Выходы

- `urllib.parse.ParseResult`
- `bool`
- `str`
- `io.BytesIO`
- `typing.Any`

## Зависимости

- `io`
- `ipaddress`
- `socket`
- `typing`
- `urllib.parse`
- `urllib.request`
- `rfc3986: uri_reference`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
