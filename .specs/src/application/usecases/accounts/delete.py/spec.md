# src/application/usecases/accounts/delete.py

## Статус

- created_at: 2026-04-02 10:00:00
- system_analyst_updated_at: 2026-04-02 10:00:00
- team_lead_synced_at: 2026-04-02 10:30:00
- backend_synced_at: 2026-04-02 10:30:00
- tester_synced_at: 2026-04-02 10:30:00
- spec_sync_synced_at: null

## Назначение

Описать сценарий удаления учётной записи текущим пользователем.

## Поведение

Модуль определяет класс `Usecase`. Сценарий принимает access-токен, декодирует из него `sub` и интерпретирует как `account_id`. По полученному идентификатору удаляет запись аккаунта через репозиторий. Если аккаунт не найден — выбрасывает `AccountNotFound`. Если токен недействителен — выбрасывает `TokenInvalid`. Метод `__call__` выполняется в write-сессии через декоратор `sessionmaker.write`. Метод `build` получает сессию и собирает контейнер зависимостей.

## Входы

- `token` — строка access JWT-токена

## Выходы

- Нет возвращаемого значения (`None`)

## Зависимости

- `src.decorators.usecases.session: sessionmaker`
- `src.domain.collections: AccountNotFound`
- `src.infrastructure.databases.orm.sqlalchemy.session: Session`
- `src.infrastructure.databases.postgres.adapters.repositories: Account`
- `src.infrastructure.security.jwt: jwt`
- `types`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Usecase не возвращает данные об удалённом аккаунте.
