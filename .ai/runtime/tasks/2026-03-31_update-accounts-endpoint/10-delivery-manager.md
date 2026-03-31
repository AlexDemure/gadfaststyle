# Delivery Manager: Update endpoint for accounts

## Описание задачи и цель

Необходимо реализовать HTTP-ручку `PATCH /api/accounts:update` для обновления данных сущности `Account`.

В проекте уже реализованы ручки:
- `POST /api/accounts:create` — создание аккаунта
- `GET /api/accounts:current` — получение текущего аккаунта
- `DELETE /api/accounts:delete` — удаление аккаунта

Ручка `update` отсутствует, хотя инфраструктура для обновления (метод `Base.update` в ORM/CRUD/репозитории) полностью готова.

**Цель:** дать аутентифицированному пользователю возможность обновлять собственные данные аккаунта через HTTP API, следуя существующим архитектурным паттернам проекта.

---

## Функциональные требования

### Поведение ручки

1. Ручка доступна только аутентифицированным пользователям (JWT Bearer token).
2. Пользователь может обновлять только **свой собственный** аккаунт — идентификатор берётся из JWT-токена через зависимость `account` (`src/entrypoints/http/common/deps/accounts/session.py`).
3. Заблокированный аккаунт (`blocked != None`) не может выполнять обновление — ошибка `AccountBlocked`.
4. Аккаунт должен существовать — при отсутствии возвращается `AccountNotFound`.
5. Поле `external_id` является чувствительным (`__encrypted__`) и должно шифроваться перед сохранением через `encryption.encrypt`.
6. При обновлении поле `updated` выставляется автоматически — это делает метод `Base.update` репозитория (`src/infrastructure/databases/postgres/adapters/repositories/base.py`, строка 67).
7. Ручка возвращает `HTTP 204 No Content` при успехе (аналогично `delete`).

### Обновляемые поля

Единственное изменяемое пользователем поле в модели `Account` (таблица `account`) — `external_id`. Поля `created`, `id`, `blocked`, `authorization` не должны быть доступны для изменения через эту ручку.

---

## Цепочка прохождения данных

Следует существующему паттерну проекта:

```
schemas -> deps -> endpoint -> usecase -> adapter -> crud -> table
```

### Файлы к созданию

| Слой | Путь |
|---|---|
| Schema | `src/entrypoints/http/public/schemas/accounts.py` — добавить `UpdateAccount` |
| Dep | `src/entrypoints/http/public/deps/accounts/update.py` |
| Router | `src/entrypoints/http/public/routers/accounts/update.py` |
| Usecase | `src/application/usecases/accounts/update.py` |

### Файлы к изменению

| Файл | Изменение |
|---|---|
| `src/entrypoints/http/public/schemas/__init__.py` | Экспортировать `UpdateAccount` |
| `src/entrypoints/http/public/deps/accounts/__init__.py` | Экспортировать зависимость `update` |
| `src/entrypoints/http/public/routers/accounts/registry.py` | Подключить `update.router` |

---

## Acceptance Criteria

### AC-1: Успешное обновление
- **Given:** пользователь авторизован (валидный JWT), аккаунт не заблокирован
- **When:** отправляет `PATCH /api/accounts:update` с телом `{"external_id": "<new_value>"}`
- **Then:** возвращается `HTTP 204 No Content`, поле `external_id` в БД обновлено (зашифровано), поле `updated` обновлено

### AC-2: Неавторизованный запрос
- **Given:** запрос без JWT или с невалидным токеном
- **When:** `PATCH /api/accounts:update`
- **Then:** возвращается `HTTP 401 Unauthorized`

### AC-3: Заблокированный аккаунт
- **Given:** пользователь авторизован, но аккаунт имеет `blocked != None`
- **When:** `PATCH /api/accounts:update`
- **Then:** возвращается ошибка `AccountBlocked` (HTTP 4xx согласно коду ошибки в `HTTPError`)

### AC-4: Аккаунт не найден
- **Given:** JWT валиден, но аккаунт с данным `id` не существует в БД
- **When:** `PATCH /api/accounts:update`
- **Then:** возвращается ошибка `AccountNotFound`

### AC-5: Шифрование
- **Given:** пользователь передаёт `external_id` в открытом виде
- **When:** запрос обрабатывается
- **Then:** в БД `external_id` сохранён в зашифрованном виде (через `encryption.encrypt`)

### AC-6: Интеграционный тест
- Создан тест по образцу `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py`
- Путь: `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py`
- Тест проверяет успешный сценарий: создать аккаунт, авторизоваться, выполнить update, убедиться что `HTTP 204`

---

## Технические ограничения и контекст проекта

### Технологический стек
- **Framework:** FastAPI (async)
- **ORM:** SQLAlchemy (async) + Alembic для миграций
- **БД:** PostgreSQL
- **Аутентификация:** JWT (Bearer token)
- **Шифрование:** кастомный модуль `src/infrastructure/security/encryption`
- **Тесты:** pytest + httpx (`AsyncClient`)

### Архитектурные паттерны

1. **Usecase** — класс с методами `build(session)` и `__call__(session, ...)`. Декоратор `@sessionmaker.write` управляет сессией.
2. **Sessionmaker:** операции записи используют `@sessionmaker.write`, чтения — `@sessionmaker.read`.
3. **Dep:** минимальная фабрика `def dependency() -> Usecase: return Usecase()`.
4. **Router:** использует `src.framework.routing.APIRouter`, стиль именования ручек — `/accounts:action`.
5. **Схемы запроса** наследуются от `Public, Request, Command`; схемы ответа — от `Public, Response`.
6. **Шифрование в usecase:** поля из `Account.__encrypted__` шифруются через `Account.encrypt(encrypter=..., ...)` перед записью.
7. **Обновление в репозитории:** метод `repository.account.update(id=account_id, **kwargs)` автоматически добавляет `updated=date.now()`.
8. **Авторизация:** зависимость `account` из `src.entrypoints.http.common.deps` возвращает `Account` текущего пользователя; при невалидном токене — 401, при `blocked` — `AccountBlocked`.

### Ограничения

- **Миграции не нужны** — схема таблицы `account` не меняется.
- Нельзя обновлять поля `id`, `created`, `blocked`, `authorization` через эту ручку.
- Имя ручки должно следовать принятому соглашению: `/accounts:update` (не `/accounts/{id}`).
- `external_id` в фильтрах поиска (метод `exists`) использует зашифрованное значение — при проверке уникальности нового `external_id` нужно шифровать перед сравнением.

### Проверка уникальности при обновлении external_id

Поле `external_id` имеет ограничение `unique=True` в таблице. Если передаётся новый `external_id`, необходимо убедиться, что он не занят другим аккаунтом. Логика аналогична `create.py`: `repository.account.exists(Filter.eq(key="external_id", value=encryption.encrypt(external_id.lower())))`, но с дополнительным условием — исключить текущий аккаунт из проверки (или проверять только если значение изменилось).

---

## Связанные файлы для изучения

- `src/application/usecases/accounts/create.py` — эталонный usecase с шифрованием
- `src/application/usecases/accounts/delete.py` — эталонный usecase для write-операции без возврата данных
- `src/entrypoints/http/public/routers/accounts/delete.py` — эталонный router с авторизацией и 204
- `src/entrypoints/http/public/schemas/accounts.py` — существующие схемы
- `src/infrastructure/databases/postgres/adapters/repositories/base.py` — метод `update`
- `src/infrastructure/databases/orm/sqlalchemy/crud/base.py` — метод `update` на уровне ORM
