# src/entrypoints/http/public/routers/accounts/delete.py

## Статус

- created_at: 2026-04-02 10:00:00
- system_analyst_updated_at: 2026-04-02 10:00:00
- team_lead_synced_at: 2026-04-02 10:30:00
- backend_synced_at: 2026-04-02 10:30:00
- tester_synced_at: 2026-04-02 10:30:00
- spec_sync_synced_at: null

## Назначение

Описать public HTTP-ручку удаления текущего аккаунта.

## Поведение

Ручка принимает bearer JWT через dependency, вызывает usecase удаления текущего аккаунта и возвращает HTTP 204 No Content по маршруту `DELETE /api/accounts:current`. При отсутствии или недействительности токена возвращает ошибки из `AUTHORIZATION_ERRORS`. При отсутствии аккаунта возвращает `AccountNotFound`.

## Входы

- `usecase`
- `token`

## Выходы

- HTTP 204 No Content (тело ответа отсутствует)

## Зависимости

- `fastapi: Depends`
- `fastapi: Response`
- `fastapi: status`
- `src.application.usecases.accounts.delete: Usecase`
- `src.domain.collections: AccountNotFound`
- `src.entrypoints.http.common.collections: AUTHORIZATION_ERRORS`
- `src.entrypoints.http.common.deps: jwt`
- `src.entrypoints.http.public.deps.accounts.delete: dependency`
- `src.framework.openapi.utils.specification: errors`
- `src.framework.routing: APIRouter`

## Ограничения

- В декораторе ручки должен быть указан `description`.
- Ручка не должна работать с БД и JWT-клиентом напрямую.
- Ручка не возвращает тело ответа.
- HTTP-статус ответа — строго 204.
