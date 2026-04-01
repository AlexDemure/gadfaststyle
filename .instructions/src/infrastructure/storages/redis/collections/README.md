## Описание

`redis/collections` описывает коллекции Redis-слоя.

## Правила

- В `collections` держи только enum, исключения и наборы значений Redis-слоя.
- Не смешивай их с клиентской реализацией.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.storages.redis.collections import exceptions
```
