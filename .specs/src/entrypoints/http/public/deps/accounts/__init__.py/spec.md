# src/entrypoints/http/public/deps/accounts/__init__.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт dependency-модулей аккаунта.

## Поведение

Файл экспортирует `create` и `current`, чтобы public account dependency подключались через один пакетный вход.

## Входы

- Импортируемые объекты пакета: `create`, `current`

## Выходы

- Публичный импорт `create`
- Публичный импорт `current`

## Зависимости

- `create: dependency as create`
- `current: dependency as current`

## Ограничения

- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
