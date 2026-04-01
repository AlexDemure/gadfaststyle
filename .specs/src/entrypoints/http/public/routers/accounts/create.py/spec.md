# src/entrypoints/http/public/routers/accounts/create.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:54:53

## Назначение

Описать HTTP-ручку `create`.

## Поведение

Модуль определяет функции: `command`. Ручка принимает HTTP-вход, вызывает соответствующий сценарий и возвращает контракт ответа.

## Входы

- `usecase`
- `body`

## Выходы

- `Tokens`

## Зависимости

- `fastapi: Body`
- `fastapi: Depends`
- `fastapi: status`
- `src.application.usecases.accounts.create: Usecase`
- `src.domain.collections: AccountAlreadyExists`
- `src.entrypoints.http.public.deps.accounts.create: dependency`
- `src.entrypoints.http.public.schemas: CreateAccount`
- `src.framework.openapi.utils.specification: errors`
- `src.framework.routing: APIRouter`
- `src.infrastructure.security.jwt.models: Tokens`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- В декораторе ручки должен быть указан `description`.
