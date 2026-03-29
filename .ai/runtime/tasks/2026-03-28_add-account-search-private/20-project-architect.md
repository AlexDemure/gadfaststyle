# Project Architect

## Architecture Context

Сценарий относится к приватному HTTP-контуру `src/entrypoints/http/system`. Для него уже используется общий router registry с `basic` authentication на префиксе `/api/-`. Для `accounts` ранее уже существовал доменный срез в `application/usecases/accounts`, а в `system`-контуре остались точки интеграции через `deps`, `routers`, `schemas` и зеркальные интеграционные тесты.

Путь данных для новой выборки:

`SearchAccount schema -> system dependency -> system router /accounts:search -> application usecase -> postgres adapter repository.paginated(...) -> response schema`

Новый сценарий должен следовать уже принятому паттерну `search`:

- request-схема с `filters`, `sorting`, `pagination`
- usecase без лишней бизнес-обработки, кроме необходимой сборки инфраструктурных запросов и пост-обработки результата
- сортировка ограничена `created`
- фильтрация по `id` точная
- тесты лежат в зеркале `tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/`

## Todo List

| Status | Executor | Description |
|---|---|---|
| todo | 40-code-implementer | Добавить `src/application/usecases/accounts/search.py` с пагинацией, сортировкой по `created` и точным фильтром по `id`. |
| todo | 40-code-implementer | Подключить приватную ручку `POST /api/-/accounts:search` через `src/entrypoints/http/system/deps/accounts/search.py`, `src/entrypoints/http/system/routers/accounts/search.py`, `src/entrypoints/http/system/routers/accounts/registry.py`. |
| todo | 40-code-implementer | Добавить системные схемы `SearchAccount` и `Accounts` в `src/entrypoints/http/system/schemas/accounts.py` и экспортировать их через `src/entrypoints/http/system/schemas/__init__.py`. |
| todo | 50-test-writer | Добавить интеграционные тесты на сортировку `created` desc/asc, точный фильтр по `id`, пагинацию и basic auth в `tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_search.py`. |
| todo | 40-code-implementer, 50-test-writer | Прогнать `python .scripts/lints/run.py` и зафиксировать результат. |
| todo | 60-code-reviewer | Проверить реализацию на регрессии маршрутизации, корректность контракта схем и тестовые пробелы. |
