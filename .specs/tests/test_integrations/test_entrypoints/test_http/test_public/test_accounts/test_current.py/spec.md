# tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_current.py

## Статус

- created_at: 2026-04-01 12:52:43
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: null
- tester_synced_at: 2026-04-01 12:52:43
- spec_sync_synced_at: null

## Назначение

Проверить public HTTP-ручку получения текущего аккаунта.

## Поведение

Интеграционные тесты должны подтверждать успешный ответ `GET /api/accounts:current` с bearer-токеном и отказ `403`, если токен не передан.

## Входы

- `client`
- `app`

## Выходы

- Подтверждение HTTP-контракта ручки `accounts:current`

## Зависимости

- `httpx: AsyncClient`
- `src.domain.models: Account`
- `src.entrypoints.http.public.deps.accounts.current: dependency`
- `src.entrypoints.http.public.schemas: CurrentAccount`

## Ограничения

- Тесты должны работать только через public HTTP-контур и не дублировать unit-проверки usecase.
