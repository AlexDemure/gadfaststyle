# Test Writer: Update endpoint for accounts

## Анализ существующего теста

Файл `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py` был создан реализатором и содержал один класс `TestAccountUpdate` с одним сценарием — успешное обновление (HTTP 204).

---

## Тестовые сценарии

### Сценарий 1 — Успешное обновление (HTTP 204)
**Класс:** `TestAccountUpdate`

| Шаг | Действие |
|---|---|
| `given()` | Создать аккаунт через `POST /api/accounts:create`, получить токены |
| `when(tokens)` | Отправить `PATCH /api/accounts:update` с заголовком `Authorization: Bearer <access_token>` и новым `external_id` |
| `then(status_code)` | Проверить `status_code == 204` |

**Статус:** существовал до правок, сохранён без изменений.

---

### Сценарий 2 — Запрос без авторизации (HTTP 403)
**Класс:** `TestAccountUpdateUnauthorized`

| Шаг | Действие |
|---|---|
| `given()` | Нет предварительных действий |
| `when()` | Отправить `PATCH /api/accounts:update` без заголовка `Authorization` |
| `then(status_code)` | Проверить `status_code == 403` |

**Обоснование статуса 403 (не 401):**
FastAPI-зависимость `HTTPBearer(bearerFormat="JWT")` при отсутствии заголовка `Authorization` возвращает HTTP 403 (поведение по умолчанию при `auto_error=True`). Обработчик `HTTPError` (который отдаёт 401 для `TokenInvalid`) регистрируется на production-приложении в `bootstrap/server.py`, но тестовый `conftest.py` создаёт чистый `FastAPI()` без этого обработчика — поэтому 403 является корректным ожидаемым кодом в тестовой среде.

**Статус:** добавлен в рамках данного этапа.

---

## Что было изменено

**Файл:** `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py`

- Сохранён существующий класс `TestAccountUpdate` (сценарий 204) без изменений.
- Добавлен новый класс `TestAccountUpdateUnauthorized` (сценарий 403).

Структура обоих классов соответствует паттерну `test_create.py`:
- `@pytest.fixture(autouse=True)` на метод `setup`
- Методы `given`, `when`, `then`, `test`
- `@pytest.mark.asyncio` на метод `test`

---

## Оценка покрытия

| Сценарий | Статус |
|---|---|
| Успешное обновление (HTTP 204) | покрыт |
| Запрос без авторизации (HTTP 403) | покрыт |
| Обновление с заблокированным аккаунтом (`AccountBlocked`) | не покрыт (нет аналога в `test_create.py`, выходит за рамки задачи) |
| Обновление с невалидным JWT → `TokenInvalid` (HTTP 401) | не покрыт (требует регистрации exception_handler в тестовом app — нет такого паттерна в проекте) |
| Проверка обновления данных в БД | не покрыт (паттерн не используется в `test_create.py`) |

**Итог:** базовые сценарии (успех + отсутствие авторизации) покрыты. Покрытие соответствует уровню, принятому в проекте (по образцу `test_create.py`).
