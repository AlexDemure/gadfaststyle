# Code Implementer: Update endpoint for accounts

## Созданные и изменённые файлы

### Созданные файлы

1. **`src/application/usecases/accounts/update.py`**
   Usecase для обновления аккаунта. Структура `Repository / Security / Container / Usecase` полностью соответствует паттерну `create.py`. Метод `__call__` задекорирован `@sessionmaker.write`, принимает `account_id: int` и `external_id: str`, шифрует `external_id` через `Account.encrypt()` и вызывает `repository.account.update(id=account_id, **encrypted_fields)`.

2. **`src/entrypoints/http/public/deps/accounts/update.py`**
   Простая фабрика `dependency() -> Usecase`, возвращает `Usecase()`. Паттерн идентичен `delete.py`.

3. **`src/entrypoints/http/public/routers/accounts/update.py`**
   Router с обработчиком `PATCH /accounts:update`. Использует `Depends(account)` для авторизации, `Body(...)` для тела запроса типа `UpdateAccount`. Возвращает `HTTP 204 No Content`. Имя функции-обработчика — `command` (write-операция, по аналогии с `create.py`).

4. **`tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py`**
   Интеграционный тест класса `TestAccountUpdate`. Сценарий: создать аккаунт (`given`), отправить `PATCH /api/accounts:update` с JWT-заголовком и новым `external_id` (`when`), проверить `status_code == 204` (`then`).

### Изменённые файлы

5. **`src/entrypoints/http/public/schemas/accounts.py`**
   Добавлен класс `UpdateAccount(Public, Request, Command)` с полем `external_id: str` в конец файла.

6. **`src/entrypoints/http/public/schemas/__init__.py`**
   Добавлен импорт `UpdateAccount` из `.accounts` и строка `"UpdateAccount"` в список `__all__`.

7. **`src/entrypoints/http/public/routers/accounts/registry.py`**
   Добавлены `from . import update` и `router.include_router(update.router)`.

---

## Отклонения от плана

Отклонений нет. Все шаги реализованы точно по плану из артефактов `20-project-architect.md` и `30-task-orchestrator.md`.

Замечание: файл `src/entrypoints/http/public/deps/accounts/__init__.py` не изменялся — это подтверждено в `30-task-orchestrator.md` (файл пустой, другие deps через него не экспортируются).
