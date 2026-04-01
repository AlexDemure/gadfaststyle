## Описание

`logging/collections` описывает коллекции logging-слоя.

## Правила

- В `collections` держи только logging-константы и наборы значений.
- Не смешивай их с formatter-, parser- и mapper-логикой.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.monitoring.logging.collections import const
```
