# src/application/usecases/accounts/create.py

## Статус

- created_at: 2026-04-01 12:14:26
- system_analyst_updated_at: 2026-04-01 12:14:26
- team_lead_synced_at: 2026-04-01 12:14:26
- backend_synced_at: 2026-04-01 12:14:26
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Описать сценарий `create`.

## Поведение

Модуль определяет классы: `Usecase`. Сценарий инкапсулирует прикладное поведение без привязки к HTTP-слою.

## Входы

- Внутренние зависимости текущего слоя

## Выходы

- Классы `Usecase`

## Зависимости

- `src.decorators.usecases.session: sessionmaker`
- `src.domain.collections: AccountAlreadyExists`
- `src.domain.models: Account`
- `src.infrastructure.databases.orm.sqlalchemy.collections: Operator`
- `src.infrastructure.databases.orm.sqlalchemy.models: Filter`
- `src.infrastructure.databases.orm.sqlalchemy.session: Session`
- `src.infrastructure.databases.postgres.adapters.repositories: Account`
- `src.infrastructure.security.encryption: encryption`
- `src.infrastructure.security.jwt.models: Tokens`
- `src.infrastructure.security.jwt: jwt`
- `types`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
