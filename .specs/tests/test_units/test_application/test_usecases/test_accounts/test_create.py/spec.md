# tests/test_units/test_application/test_usecases/test_accounts/test_create.py

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

Модуль определяет классы: `AccountRepository`, `Encryption`, `JWT`. Модуль определяет функции: `build_container`, `test_create_account_usecase_success`, `test_create_account_usecase_duplicate`.

## Входы

- `repository`
- `monkeypatch`

## Выходы

- `types.SimpleNamespace`
- `None`
- `None`
- Классы `AccountRepository`
- Классы `Encryption`
- Классы `JWT`

## Зависимости

- `pytest`
- `src.application.usecases.accounts.create: Usecase`
- `src.domain.collections: AccountAlreadyExists`
- `src.domain.models: Account`
- `src.infrastructure.security.jwt.models: Tokens`
- `types`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
