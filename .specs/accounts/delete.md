# Удаление аккаунта

## Описание

Удаляет текущий аккаунт по access JWT-токену. Декодирует токен, извлекает `account_id` и удаляет запись. Если аккаунт не найден — поднимает `AccountNotFound`.

## Задачи

| # | Область | Описание |
|---|---------|----------|
| 1 | Backend | Usecase, dependency, роутер |
| 2 | Testing | Интеграционный тест DELETE /api/accounts:current |

---

## Backend

### Схема взаимодействия

```mermaid
graph TD
    Client[HTTP Client]
    Router[DELETE /api/accounts:current]
    JWTDep[deps / security / jwt]
    Dep[deps / accounts / delete]
    UC[usecases / accounts / delete]
    Repo[postgres / adapters / repositories / account]
    JWT[infrastructure / security / jwt]
    Exc[domain / collections / AccountNotFound]
    DB[(PostgreSQL)]

    Client -->|Authorization: Bearer| Router
    Router --> JWTDep
    Router --> Dep --> UC
    UC --> JWT
    UC --> Repo --> DB
    UC --> Exc
```

### Задачи

| # | Слой | Путь | Действие | Описание |
|---|------|------|----------|----------|
| 1 | application | src/application/usecases/accounts/delete.py | create | Usecase: декодирование JWT → `account_id`, удаление; `AccountNotFound` если не найден |
| 2 | entrypoint | src/entrypoints/http/public/deps/accounts/delete.py | create | Dependency-фабрика usecase удаления |
| 3 | entrypoint | src/entrypoints/http/public/routers/accounts/delete.py | create | `DELETE /api/accounts:current` → HTTP 204, без тела ответа |

---

## Testing

### Схема взаимодействия

```mermaid
graph TD
    Factory[factories / domain / models / Account]
    Client[AsyncClient]
    Router[DELETE /api/accounts:current]
    UC[usecases / accounts / delete]
    DB[(Test PostgreSQL)]

    Factory --> DB
    Factory --> Client
    Client -->|Bearer token| Router --> UC --> DB
```

### Задачи

| # | Слой | Путь | Действие | Описание |
|---|------|------|----------|----------|
| 1 | tests | tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_delete.py | create | Тест: успешное удаление → HTTP 204; повторный запрос → 4xx |
