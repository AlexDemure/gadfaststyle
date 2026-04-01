## Описание

`encryption/collections` описывает коллекции encryption-слоя.

## Правила

- В `collections` держи только технические исключения и наборы значений.
- Не смешивай их с реализацией шифрования.
- Публичные элементы экспортируй через пакет.

## Примеры

```python
from src.infrastructure.security.encryption.collections import exceptions
```
