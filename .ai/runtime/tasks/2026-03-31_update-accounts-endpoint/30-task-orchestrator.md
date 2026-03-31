# Task Orchestrator: Update endpoint for accounts

## Проверка актуальности плана

Реальный код проверен. Все импорты, структуры классов и паттерны из артефактов предыдущих этапов подтверждены:

- `src/application/usecases/accounts/create.py` и `delete.py` — эталонная структура `Repository / Security / Container / Usecase` совпадает с планом.
- `src/entrypoints/http/public/deps/accounts/__init__.py` — файл **пустой** (0 байт). Экспортировать зависимость `update` из него не требуется — никакие другие deps там не экспортируются. Шаг изменения этого файла **исключён**.
- `src/entrypoints/http/public/schemas/__init__.py` — экспортирует `CreateAccount` и `CurrentAccount`. Нужно добавить `UpdateAccount`.
- `src/entrypoints/http/public/routers/accounts/registry.py` — подключает `create`, `current`, `delete`. Нужно добавить `update`.
- `Base.update(id, **kwargs)` в репозитории — автоматически добавляет `updated=date.now()` (строка 67, подтверждено).
- `Account.__encrypted__ = ["external_id"]` и `Account.encrypt(encrypter=..., **kwargs)` — работают как описано.
- Тест создаётся по образцу `test_create.py` с JWT-авторизацией.

---

## Атомарный план выполнения (checklist)

### Шаг 1 — Создать usecase
**Файл:** `src/application/usecases/accounts/update.py` (создать новый)  
**Действие:** создать файл со структурой `Repository / Security / Container / Usecase`.  
**Содержимое:**
- Класс `Repository` — инициализирует `self.account = adapters.repositories.Account(session)`
- Класс `Security` — инициализирует `self.encryption = encryption`
- Класс `Container` — принимает `repository` и `security`
- Класс `Usecase` — метод `build(session)`, метод `__call__` задекорированный `@sessionmaker.write`, принимает `account_id: int, external_id: str`, вызывает `repository.account.update(id=account_id, **Account.encrypt(encrypter=..., external_id=external_id))`
- Возвращает `None` (нет return value)

**Зависимости:** нет, файл независим.

---

### Шаг 2 — Создать dep
**Файл:** `src/entrypoints/http/public/deps/accounts/update.py` (создать новый)  
**Действие:** создать файл с фабричной функцией `dependency() -> Usecase`.  
**Содержимое:**
```python
from src.application.usecases.accounts.update import Usecase

def dependency() -> Usecase:
    return Usecase()
```

**Зависимости:** Шаг 1 должен быть выполнен (импортируется `Usecase`).

---

### Шаг 3 — Добавить схему `UpdateAccount`
**Файл:** `src/entrypoints/http/public/schemas/accounts.py` (изменить — добавить в конец)  
**Действие:** добавить новый класс после `CurrentAccount`:
```python
class UpdateAccount(Public, Request, Command):
    external_id: str
```

**Зависимости:** нет, файл независим от шагов 1–2.

---

### Шаг 4 — Экспортировать `UpdateAccount` из `__init__.py` схем
**Файл:** `src/entrypoints/http/public/schemas/__init__.py` (изменить)  
**Действие:**
- Добавить в импорты: `from .accounts import UpdateAccount`
- Добавить `"UpdateAccount"` в список `__all__`

**Зависимости:** Шаг 3 должен быть выполнен (класс `UpdateAccount` должен существовать).

---

### Шаг 5 — Создать router
**Файл:** `src/entrypoints/http/public/routers/accounts/update.py` (создать новый)  
**Действие:** создать файл с роутером по образцу `delete.py`, но:
- Метод: `@router.patch` (не `@router.delete`)
- Путь: `"/accounts:update"`
- Добавить параметр `body: UpdateAccount = Body(...)` (импорт `from fastapi import Body`)
- Вызов usecase: `await usecase(account_id=field.required(_account.id), **body.deserialize())`
- Имя функции-обработчика: `command` (аналогично `create.py` — операция записи)
- Импорт `UpdateAccount` из `src.entrypoints.http.public.schemas`

**Зависимости:** Шаги 2, 3 и 4 должны быть выполнены.

---

### Шаг 6 — Подключить router в registry
**Файл:** `src/entrypoints/http/public/routers/accounts/registry.py` (изменить)  
**Действие:**
- Добавить импорт: `from . import update`
- Добавить строку: `router.include_router(update.router)`

**Зависимости:** Шаг 5 должен быть выполнен.

---

### Шаг 7 — Создать интеграционный тест
**Файл:** `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py` (создать новый)  
**Действие:** создать тест по образцу `test_create.py` со следующим сценарием:
1. `given()` — создать аккаунт через `POST /api/accounts:create`, получить токены
2. `when()` — отправить `PATCH /api/accounts:update` с заголовком `Authorization: Bearer <access_token>` и телом `{"external_id": fake.uuid4()}`
3. `then()` — проверить `response.status_code == 204`

Структура класса: `TestAccountUpdate` с методами `setup`, `given`, `when`, `then`, `test`.  
Фикстуры: `client: AsyncClient`, `session: AsyncSession` (через `pytest.fixture(autouse=True)`).

**Зависимости:** Шаги 1–6 должны быть выполнены (ручка должна существовать).

---

## Граф зависимостей

```
Шаг 1 (usecase)
    └─► Шаг 2 (dep)
            └─► Шаг 5 (router) ◄── Шаг 3 (schema) ──► Шаг 4 (__init__)
                    └─► Шаг 6 (registry)
                            └─► Шаг 7 (test)
```

Шаги 1 и 3 можно выполнять параллельно — они не зависят друг от друга.

---

## Файлы, которые НЕ нужно изменять

| Файл | Причина |
|---|---|
| `src/entrypoints/http/public/deps/accounts/__init__.py` | Файл пустой, другие deps не экспортируются из него — не нужен |
| Все файлы `infrastructure/` | Метод `update` в репозитории уже существует |
| Все файлы миграций | Схема таблицы `account` не меняется |
| `src/domain/models/account.py` | `__encrypted__` и `encrypt()` уже реализованы |

---

## Замечания по реализации

1. **Имя обработчика в router:** использовать `command` (не `query`) — по аналогии с `create.py`, поскольку это write-операция.
2. **`deps/accounts/__init__.py`:** файл пустой и остаётся пустым — другие deps (create, delete) также не экспортируются через него.
3. **Уникальность `external_id`:** по анализу `delete.py` и поведению зависимости `account`, аккаунт уже загружен через `Depends(account)` — проверка `AccountNotFound` и `AccountBlocked` происходит там. В usecase достаточно просто вызвать `update`. Проверку уникальности `external_id` (упомянутую в 10-delivery-manager.md) следует добавить опционально, только если в требованиях явно указано — базовый вариант её не включает, чтобы не отклоняться от паттерна `delete.py`.
4. **Шифрование:** `Account.encrypt()` из `base.py` — только поля из `__encrypted__` (`external_id`). Результат — `{"external_id": encrypted_value}`, который передаётся как `**kwargs` в `repository.account.update`.
