# src/application/usecases/accounts/__init__.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт usecase-модулей аккаунта.

## Поведение

Файл экспортирует `CreateUsecase` и `CurrentUsecase`, чтобы account-сценарии подключались через один пакетный вход.

## Входы

- Импортируемые объекты пакета: `CreateUsecase`, `CurrentUsecase`

## Выходы

- Публичный импорт `CreateUsecase`
- Публичный импорт `CurrentUsecase`

## Зависимости

- `create: Usecase as CreateUsecase`
- `current: Usecase as CurrentUsecase`

## Ограничения

- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
