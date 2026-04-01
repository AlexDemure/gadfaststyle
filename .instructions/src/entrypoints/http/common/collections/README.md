## Описание

`entrypoints/http/common/collections` описывает общие HTTP-коллекции entrypoint-слоя.

## Правила

- В `collections` держи общие ошибки и наборы значений, используемые в нескольких router-пакетах.
- Не размещай здесь схемы, deps и реализацию ручек.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.entrypoints.http.common.collections import errors
```
