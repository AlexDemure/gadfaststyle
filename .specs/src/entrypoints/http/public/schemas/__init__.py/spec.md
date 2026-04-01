# src/entrypoints/http/public/schemas/__init__.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт public HTTP-схем.

## Поведение

Файл экспортирует `CreateAccount`, `CurrentAccount` и `Public` для использования в public HTTP-слое.

## Входы

- Импортируемые объекты пакета: `CreateAccount`, `CurrentAccount`, `Public`

## Выходы

- Публичный импорт `CreateAccount`
- Публичный импорт `CurrentAccount`
- Публичный импорт `Public`

## Зависимости

- `account: CreateAccount`
- `account: CurrentAccount`
- `base: Public`

## Ограничения

- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
