## Реализация HTTP endpoint

| Шаг | Действие | Инструкции | Результат |
| --- | --- | --- | --- |
| 1 | Определи домен и контур endpoint. | [../src/domain/instruction.md](../src/domain/instruction.md), [../src/entrypoints/http/instruction.md](../src/entrypoints/http/instruction.md) | Понятен домен, контур и операция `create/get/search/update/delete`. |
| 2 | Опиши или обнови domain model. | [../src/domain/models/instruction.md](../src/domain/models/instruction.md) | Готова модель домена. |
| 3 | Опиши domain exceptions и enum-коллекции, если они нужны. | [../src/domain/collections/exceptions/instruction.md](../src/domain/collections/exceptions/instruction.md), [../src/domain/collections/enums/instruction.md](../src/domain/collections/enums/instruction.md) | Готовы исключения и enum-ы домена. |
| 4 | Добавь таблицы базы данных для домена. | [../src/infrastructure/databases/postgres/tables/instruction.md](../src/infrastructure/databases/postgres/tables/instruction.md) | Готовы runtime table-классы. |
| 5 | Добавь CRUD-слой для домена. | [../src/infrastructure/databases/postgres/crud/instruction.md](../src/infrastructure/databases/postgres/crud/instruction.md) | Готовы CRUD-классы домена. |
| 6 | Добавь repository adapter для домена. | [../src/infrastructure/databases/postgres/adapters/instruction.md](../src/infrastructure/databases/postgres/adapters/instruction.md) | Готов adapter-слой домена. |
| 7 | Если нужны прикладные утилиты, добавь их в application. | [../src/application/utils/instruction.md](../src/application/utils/instruction.md) | Готовы общие application utils. |
| 8 | Реализуй usecase. Для mutation используй `command`, для read `query`. | [../src/application/usecases/instruction.md](../src/application/usecases/instruction.md), [../src/application/usecases/command/instruction.md](../src/application/usecases/command/instruction.md), [../src/application/usecases/query/instruction.md](../src/application/usecases/query/instruction.md) | Готов usecase. |
| 9 | Добавь HTTP schema и dependency. | [../src/entrypoints/http/common/schemas/instruction.md](../src/entrypoints/http/common/schemas/instruction.md), [../src/entrypoints/http/public/schemas/instruction.md](../src/entrypoints/http/public/schemas/instruction.md), [../src/entrypoints/http/system/schemas/instruction.md](../src/entrypoints/http/system/schemas/instruction.md), [../src/entrypoints/http/public/deps/instruction.md](../src/entrypoints/http/public/deps/instruction.md), [../src/entrypoints/http/system/deps/instruction.md](../src/entrypoints/http/system/deps/instruction.md) | Готовы schema и dependency. |
| 10 | Добавь router-операцию в нужном контуре. | [../src/entrypoints/http/public/routers/instruction.md](../src/entrypoints/http/public/routers/instruction.md), [../src/entrypoints/http/system/routers/instruction.md](../src/entrypoints/http/system/routers/instruction.md) | Готов router-файл операции. |
| 11 | Подключи публичные импорты и registry-слой, если это требуется пакетом. | Инструкции соответствующего пакета, где описан `__init__.py`, `__all__` или `registry.py`. | Новый код доступен из публичных импортов и подключен в контур. |
| 12 | Добавь тесты. | [../tests/instruction.md](../tests/instruction.md), [../tests/test_integrations/instruction.md](../tests/test_integrations/instruction.md), [../tests/test_units/instruction.md](../tests/test_units/instruction.md), [../tests/factories/instruction.md](../tests/factories/instruction.md), [../tests/mocking/instruction.md](../tests/mocking/instruction.md) | Готовы integration и unit tests, фабрики и mocks при необходимости. |
| 13 | Если схема БД изменилась, создай миграцию отдельно через Alembic. | [../src/infrastructure/databases/postgres/rules.md](../src/infrastructure/databases/postgres/rules.md) | Runtime-код и миграции разделены. |

## Порядок реализации

- Domain определяет модель и контракты.
- Infrastructure реализует хранение и интеграцию.
- Application собирает usecase поверх готовых контрактов.
- Entrypoint подключает schema, dependency и router.
- Tests проверяют итоговый сценарий.
