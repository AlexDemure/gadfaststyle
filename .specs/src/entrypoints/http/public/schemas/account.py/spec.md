# src/entrypoints/http/public/schemas/account.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Описать request и response схемы аккаунта для public HTTP-контура.

## Поведение

Файл содержит `CreateAccount` для входа в ручку создания и `CurrentAccount` для сериализации текущего аккаунта в ответе.

## Входы

- `external_id`
- Доменная модель `Account` для сериализации

## Выходы

- Схема `CreateAccount`
- Схема `CurrentAccount`

## Зависимости

- `src.domain.models: Account as Model`
- `src.entrypoints.http.common.schemas: Command`
- `src.entrypoints.http.common.schemas: Query`
- `src.entrypoints.http.common.schemas: Request`
- `src.entrypoints.http.common.schemas: Response`
- `base: Public`

## Ограничения

- Схемы должны описывать только HTTP-контракт и сериализацию без бизнес-логики.
