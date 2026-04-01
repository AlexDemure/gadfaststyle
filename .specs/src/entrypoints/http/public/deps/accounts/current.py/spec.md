# src/entrypoints/http/public/deps/accounts/current.py

## Статус

- created_at: 2026-04-01 12:52:43
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: null

## Назначение

Поднять dependency для usecase получения текущего аккаунта.

## Поведение

Dependency создает экземпляр `Usecase` для ручки чтения текущего аккаунта.

## Входы

- Нет внешних входов.

## Выходы

- Экземпляр `Usecase`

## Зависимости

- `src.application.usecases.accounts.current: Usecase`

## Ограничения

- Dependency не должен содержать бизнес-логику и инфраструктурные детали вне сборки usecase.
