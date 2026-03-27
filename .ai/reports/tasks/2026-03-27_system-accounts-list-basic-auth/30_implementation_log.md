# Implementation Log

## Измененные файлы

- `src/application/usecases/accounts/list.py` - добавлен read usecase списка аккаунтов с расшифрованием `external_id`
- `src/entrypoints/http/system/routers/registry.py` - подключен новый system accounts router под `http-basic`
- `src/entrypoints/http/system/routers/accounts/*.py` - добавлен router домена и endpoint списка
- `src/entrypoints/http/system/deps/accounts/*.py` - добавлена DI-фабрика usecase
- `src/entrypoints/http/system/schemas/accounts.py` - добавлены response schema списка

## Архитектурные решения

- В качестве пользователей используется доменная сущность `Account`.
- Endpoint размещен в `system`, потому что это служебное чтение для администраторов.
- Защита подключена через существующий `basic` dependency на уровне include_router.
- Для стабильного списка используется `paginated(...)` и сортировка по `created desc`.

## Примечания

- Ответ сделан в формате `total + items`, потому что в проекте уже есть общая схема `Paginated`.
