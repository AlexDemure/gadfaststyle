## Описание

`factories/infrastructure` описывает фабрики инфраструктурных объектов для тестов.

## Правила

- Здесь создавай table-модели, payload-объекты и технические данные инфраструктуры.
- Фабрики должны быть быстрыми и детерминированными.
- Не смешивай их с domain-фабриками.

## Примеры

```python
from tests.factories.infrastructure.databases.postgres import tables
```
