# src/entrypoints/http/common/schemas/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `schemas`.

## Поведение

Файл собирает и экспортирует: `Command`, `DateRange`, `ID`, `Paginated`, `Pagination`, `Photo`, `Query`, `Request`, `Response`, `Sorted`, `URL`.

## Входы

- Импортируемые объекты пакета: `Command`, `DateRange`, `ID`, `Paginated`, `Pagination`, `Photo`, `Query`, `Request`, `Response`, `Sorted`, `URL`

## Выходы

- Публичный импорт `Command`
- Публичный импорт `DateRange`
- Публичный импорт `ID`
- Публичный импорт `Paginated`
- Публичный импорт `Pagination`
- Публичный импорт `Photo`
- Публичный импорт `Query`
- Публичный импорт `Request`
- Публичный импорт `Response`
- Публичный импорт `Sorted`
- Публичный импорт `URL`

## Зависимости

- `cqrs: Command`
- `cqrs: Query`
- `dates: DateRange`
- `http: Request`
- `http: Response`
- `model: ID`
- `pagination: Paginated`
- `pagination: Pagination`
- `sorting: Sorted`
- `urls: Photo`
- `urls: URL`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
