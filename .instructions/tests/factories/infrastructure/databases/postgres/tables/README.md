## Описание

`factories/infrastructure/databases/postgres/tables` описывает фабрики Postgres-таблиц.

## Правила

- Каждая фабрика должна создавать валидный table row для тестов.
- Значения по умолчанию должны подходить для большинства сценариев слоя хранения.
- Не добавляй сюда domain-логику.

## Примеры

```python
from tests.factories.infrastructure.databases.postgres.tables import Account
```
