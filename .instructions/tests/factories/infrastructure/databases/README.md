## Описание

`factories/infrastructure/databases` описывает фабрики слоя БД для тестов.

## Правила

- Разделяй фабрики по реализациям БД и типам хранилищ.
- Фабрики должны создавать технические данные слоя хранения.
- Не размещай здесь domain-модели.

## Примеры

```python
from tests.factories.infrastructure.databases import postgres
```
