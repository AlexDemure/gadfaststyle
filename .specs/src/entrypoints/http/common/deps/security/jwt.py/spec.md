# src/entrypoints/http/common/deps/security/jwt.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать зависимости и сборку контекста модуля `src/entrypoints/http/common/deps/security/jwt.py`.

## Поведение

Модуль определяет Функции: `dependency`.

## Входы

- `authorization`
- `Depends(HTTPBearer(bearerFormat`

## Выходы

- `str`

## Зависимости

- `typing`
- `fastapi: Depends`
- `fastapi.security: HTTPAuthorizationCredentials`
- `fastapi.security: HTTPBearer`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
