# tests/test_units/test_application/test_usecases/test_accounts/test_current.py

## Статус

- created_at: 2026-04-01 12:52:43
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: null
- tester_synced_at: 2026-04-01 12:52:43
- spec_sync_synced_at: null

## Назначение

Проверить usecase получения текущего аккаунта.

## Поведение

Юнит-тесты должны проверять успешное чтение аккаунта с расшифровкой `external_id` и ошибку `TokenInvalid`, если `sub` в JWT не приводится к целочисленному id.

## Входы

- `monkeypatch`

## Выходы

- Подтверждение поведения usecase `current`

## Зависимости

- `pytest`
- `src.application.usecases.accounts.current: Usecase`
- `src.domain.collections: AccountNotFound`
- `src.domain.models: Account`
- `src.infrastructure.security.jwt.collections: TokenInvalid`
- `src.infrastructure.security.jwt.collections: TokenPurpose`
- `src.infrastructure.security.jwt.models: Token`
- `types`

## Ограничения

- Тесты должны проверять только поведение usecase и не использовать HTTP-контур.
