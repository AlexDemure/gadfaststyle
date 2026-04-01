## Описание

`mocking/infrastructure/storages` описывает mock-объекты storage-слоя.

## Правила

- Каждый mock покрывает один storage-контракт.
- Поведение mock должно быть предсказуемым и минимальным.
- Не размещай здесь моки БД и HTTP-моки.

## Примеры

```python
from tests.mocking.infrastructure.storages import redis
```
