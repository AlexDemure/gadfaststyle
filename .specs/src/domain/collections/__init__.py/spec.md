# src/domain/collections/__init__.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `collections`.

## Поведение

Файл собирает и экспортирует: `AccountAlreadyExists`, `AccountBlocked`, `AccountNotFound`.

## Входы

- Импортируемые объекты пакета: `AccountAlreadyExists`, `AccountBlocked`, `AccountNotFound`

## Выходы

- Публичный импорт `AccountAlreadyExists`
- Публичный импорт `AccountBlocked`
- Публичный импорт `AccountNotFound`

## Зависимости

- `exceptions: AccountAlreadyExists`
- `exceptions: AccountBlocked`
- `exceptions: AccountNotFound`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
