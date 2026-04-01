# tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: null
- tester_synced_at: 2026-04-01 12:14:26
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Описать модуль `test_create`.

## Поведение

Модуль определяет классы: `FakeUsecase`. Модуль определяет функции: `test_create_account`.

## Входы

- `client`
- `app`

## Выходы

- `None`
- Классы `FakeUsecase`

## Зависимости

- `httpx: AsyncClient`
- `src.entrypoints.http.public.deps.accounts.create: dependency`
- `src.infrastructure.security.jwt.models: Tokens`
- `tests.faker: fake`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
