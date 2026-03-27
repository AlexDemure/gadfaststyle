# Architecture: Common

## Назначение

`gadfaststyle` - backend-проект на `FastAPI` с явным разделением по слоям. Новый код должен встраиваться в уже существующую структуру, а не создавать новую.

## Порядок чтения для любого агента

1. Прочитай этот файл.
2. Определи, какие слои затрагивает задача.
3. Прочитай соответствующие файлы:
   - `.ai/architecture/http.md`
   - `.ai/architecture/application.md`
   - `.ai/architecture/domain.md`
   - `.ai/architecture/infrastructure.md`
   - `.ai/architecture/tests.md`
4. Только после этого открывай конкретные файлы в `src/` и `tests/`.

## Карта проекта

- `src/bootstrap/` - сборка приложения, lifecycle, middleware, подключение инфраструктуры.
- `src/configuration/` - `settings` и чтение `.env`.
- `src/entrypoints/http/` - схемы, deps, routers и registry HTTP-слоя.
- `src/application/usecases/` - бизнес-сценарии.
- `src/domain/models/` - доменные модели.
- `src/domain/collections/exceptions/` - доменные и прикладные исключения.
- `src/infrastructure/` - БД, клиенты, security, monitoring, storage и setup-инстансы.
- `tests/test_integrations/` - HTTP-сценарии.
- `tests/factories/` - фабрики и тестовые помощники.

## Базовый поток запроса

Путь данных строится так:

`schema -> dependency -> router -> usecase -> repository adapter -> crud -> table`

Если задача не проходит через HTTP, все равно ориентируйся на этот стиль разделения ответственности.

## Общие правила по стилю

- Именование домена повторяет существующий паттерн: `accounts`, `account`, `create`, `delete`, `current`.
- Если появляется новый домен, создавай отдельную папку домена на каждом нужном слое, а не смешивай его с `accounts`.
- Импорты оформляй так же, как в существующих модулях: по одному `from ... import ...` на строку, без изобретения нового стиля.
- Новые файлы называй по операции или сущности, а не по абстракции.
- Не копируй код дословно; копируй форму, нейминг, расположение и уровень детализации.

## Как смотреть существующую реализацию

Базовый эталон для нового CRUD/HTTP-сценария:

- `src/entrypoints/http/public/routers/accounts/create.py`
- `src/entrypoints/http/public/routers/accounts/registry.py`
- `src/entrypoints/http/public/deps/accounts/create.py`
- `src/entrypoints/http/public/schemas/accounts.py`
- `src/application/usecases/accounts/create.py`
- `src/domain/models/account.py`
- `src/domain/collections/exceptions/account.py`
- `src/infrastructure/databases/postgres/adapters/repositories/account.py`
- `src/infrastructure/databases/postgres/crud/account.py`
- `src/infrastructure/databases/postgres/tables/account.py`
- `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py`

## Когда создавать новую папку

- Новый бизнес-домен в HTTP: новая папка в `src/entrypoints/http/public/routers/<domain>/` и `deps/<domain>/`.
- Новый usecase-домен: новая папка в `src/application/usecases/<domain>/`.
- Новая доменная сущность: новый файл в `src/domain/models/` и при необходимости в `src/domain/collections/exceptions/`.
- Новый инфраструктурный клиент: новая папка внутри соответствующего раздела `src/infrastructure/...`.
- Новый HTTP-домен в тестах: зеркальная папка в `tests/test_integrations/test_entrypoints/test_http/test_public/test_<domain>/`.

## Что запрещено

- Не писать бизнес-логику в router.
- Не писать SQL или прямую работу с таблицами в usecase.
- Не создавать новые naming conventions рядом с уже установленными.
- Не смешивать тестовый и production-код в одном слое.
