# src/common/formats/utils/date.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/common/formats/utils/date.py`.

## Поведение

Модуль определяет Функции: `now`, `midnight`, `today`, `previous`, `tostring`, `fromstring`, `before`, `after`, `include`, `same`, `diff`, `age`, `iso`, `short`, `full`, `human`, `time`, `us`, `eu`, `rfc2822`, `rfc3339`, `start`, `end`, `weekend`, `shift`.

## Входы

- `date`
- `fmt`
- `comparison`
- `seconds`
- `minutes`
- `hours`
- `days`

## Выходы

- `datetime.datetime`
- `datetime.date`
- `str`
- `bool`
- `datetime.timedelta`
- `int`

## Зависимости

- `datetime`
- `src.common.formats.collections: Format`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
