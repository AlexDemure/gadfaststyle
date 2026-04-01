# src/entrypoints/http/public/routers/accounts/current.py

## Статус

- created_at: 2026-04-01 12:52:43
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: null

## Назначение

Описать public HTTP-ручку чтения текущего аккаунта.

## Поведение

Ручка принимает bearer JWT через dependency, вызывает usecase получения текущего аккаунта и возвращает сериализованный `CurrentAccount` по маршруту `GET /api/accounts:current`.

## Входы

- `usecase`
- `token`

## Выходы

- HTTP-ответ `CurrentAccount`

## Зависимости

- `src.application.usecases.accounts.current: Usecase`
- `src.domain.collections.AccountNotFound`
- `src.entrypoints.http.common.collections.AUTHORIZATION_ERRORS`
- `src.entrypoints.http.common.deps: jwt`
- `src.entrypoints.http.public.deps.accounts.current: dependency`
- `src.entrypoints.http.public.schemas: CurrentAccount`
- `src.framework.openapi.utils.specification: errors`
- `src.framework.routing: APIRouter`

## Ограничения

- В декораторе ручки должен быть указан `description`.
- Ручка не должна работать с БД и JWT-клиентом напрямую.
