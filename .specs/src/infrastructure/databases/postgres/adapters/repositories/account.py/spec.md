# src/infrastructure/databases/postgres/adapters/repositories/account.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:52:43
- team_lead_synced_at: 2026-04-01 12:52:43
- backend_synced_at: 2026-04-01 12:52:43
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Адаптировать account persistence к доменной модели аккаунта.

## Поведение

Repository adapter связывает CRUD и table account с доменной моделью `Account` и должен поднимать `AccountNotFound`, если чтение аккаунта не находит запись.

## Входы

- Фильтры чтения и проверки существования account

## Выходы

- Доменная модель `Account` или доменная ошибка поиска

## Зависимости

- `src.domain.collections.AccountNotFound`
- `src.domain: models`
- `src.infrastructure.databases.postgres: crud`
- `src.infrastructure.databases.postgres: tables`
- `src.infrastructure.databases.postgres.adapters.repositories.base: Base`
- `src.infrastructure.databases.orm.sqlalchemy.models: Filter`
- `src.infrastructure.databases.orm.sqlalchemy.models: And`
- `src.infrastructure.databases.orm.sqlalchemy.models: Or`

## Ограничения

- Repository adapter не должен содержать HTTP-логику и должен возвращать доменные ошибки account-слоя.
