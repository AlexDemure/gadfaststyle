## Описание

`framework/openapi/collections` описывает коллекции OpenAPI-слоя.

## Правила

- В `collections` держи только константы и фиксированные наборы значений OpenAPI.
- Не размещай здесь handlers, models и utils.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.framework.openapi.collections import const
```
