# Technical Plan

## Подзадачи

1. Добавить новый system-домен `accounts` с отдельным `registry.py` и `list.py`.
2. Добавить dependency и usecase для чтения списка аккаунтов.
3. Добавить response schema для списка аккаунтов.
4. Подключить system-router домена через existing registry и защитить `http-basic`.
5. Добавить интеграционный тест на успешный ответ и отказ без корректного `http-basic`.

## Карта файлов

- `src/entrypoints/http/system/routers/registry.py` - подключение system accounts router с basic dependency
- `src/entrypoints/http/system/routers/accounts/*.py` - endpoint и registry домена
- `src/entrypoints/http/system/deps/accounts/*.py` - dependency usecase
- `src/entrypoints/http/system/schemas/accounts.py` - response model
- `src/application/usecases/accounts/list.py` - чтение и расшифрование аккаунтов
- `tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_list.py` - HTTP-тест

## Критерии готовности

- `GET /api/-/accounts?page=1&size=10` возвращает список аккаунтов и `total`.
- Endpoint требует корректный `http-basic`.
- `external_id` в ответе расшифрован.
- Есть интеграционный тест на happy path и unauthorized.
