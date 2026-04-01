## Описание

`framework/collections` описывает общие коллекции framework-слоя.

## Правила

- В `collections` держи framework-константы и исключения.
- Не смешивай их с routing, openapi и background-реализациями.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.framework.collections import exceptions
```
