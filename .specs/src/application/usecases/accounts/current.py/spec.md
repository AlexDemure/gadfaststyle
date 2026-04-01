# src/application/usecases/accounts/current.py

## Статус

- created_at: 2026-04-01 12:52:43
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: null

## Назначение

Получить текущий аккаунт по access JWT-токену.

## Поведение

Usecase принимает bearer-токен, декодирует access-подпись, читает аккаунт по `sub`, расшифровывает `external_id` и возвращает доменную модель текущего аккаунта.

## Входы

- `token`

## Выходы

- Доменная модель текущего `Account`

## Зависимости

- `src.domain.models.Account`
- `src.infrastructure.databases.postgres.adapters.repositories.Account`
- `src.infrastructure.security.encryption`
- `src.infrastructure.security.jwt`
- `src.infrastructure.security.jwt.collections.TokenInvalid`
- `src.infrastructure.security.jwt.collections.TokenPurpose`

## Ограничения

- Usecase должен принимать только access-токен.
- Usecase не работает с HTTP-слоем напрямую.
- `external_id` должен возвращаться в расшифрованном виде.
