# src/entrypoints/http/public/routers/accounts/registry.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать регистрацию public HTTP-ручек аккаунта.

## Поведение

Registry подключает router-ы `create` и `current` в общий account-контур public API.

## Входы

- Внутренние зависимости текущего слоя

## Выходы

- Подключенный router аккаунтов

## Зависимости

- `create: router`
- `current: router`
- `src.framework.routing: APIRouter`

## Ограничения

- Registry должен только подключать router-модули и не содержать обработчики операций.
