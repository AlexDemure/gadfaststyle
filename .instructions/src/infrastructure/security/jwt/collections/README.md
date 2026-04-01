## Описание

`jwt/collections` описывает коллекции JWT-слоя.

## Правила

- В `collections` держи только enum, исключения и наборы значений JWT-слоя.
- Не смешивай их с моделями и реализацией токенов.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.security.jwt.collections import exceptions
```
