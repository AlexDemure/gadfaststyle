# Architecture Context

## Целевой модуль

System HTTP endpoint для служебного списка аккаунтов.

## Куда вносить изменения

- `src/entrypoints/http/system/routers/` - новый домен `accounts` и операция `list.py`
- `src/entrypoints/http/system/deps/` - dependency для usecase списка
- `src/entrypoints/http/system/schemas/` - response schema списка
- `src/application/usecases/accounts/` - read usecase списка аккаунтов
- `tests/test_integrations/test_entrypoints/test_http/test_system/` - интеграционный HTTP-тест

## Архитектурные ограничения

- Использовать существующий `basic` dependency, а не новый механизм авторизации.
- Использовать доменную сущность `Account`, а не вводить новый `User`.
- Бизнес-логика чтения должна жить в usecase-слое.
- Для чтения `external_id` нужно использовать существующее расшифрование.
