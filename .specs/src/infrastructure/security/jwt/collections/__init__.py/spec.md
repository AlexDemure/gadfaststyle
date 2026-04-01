# src/infrastructure/security/jwt/collections/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `collections`.

## Поведение

Файл собирает и экспортирует: `ClientDisabled`, `TokenInvalid`, `TokenPurpose`.

## Входы

- Импортируемые объекты пакета: `ClientDisabled`, `TokenInvalid`, `TokenPurpose`

## Выходы

- Публичный импорт `ClientDisabled`
- Публичный импорт `TokenInvalid`
- Публичный импорт `TokenPurpose`

## Зависимости

- `enums: TokenPurpose`
- `exceptions: ClientDisabled`
- `exceptions: TokenInvalid`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
