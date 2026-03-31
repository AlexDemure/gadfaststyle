## Описание

`collections` описывает доменные коллекции.

## Правила

- Исключения держи в `exceptions/`, enum и фиксированные наборы значений держи в `enums/`.
- Публичные элементы collections экспортируй через `collections/__init__.py`.
- Если код должен писать `from src.domain.collections import AccountNotFound`, экспорт уже должен быть собран в пакете.
- Не складывай сюда прикладные утилиты и инфраструктурный код.

## Примеры

```python
from src.domain.collections import AccountAlreadyExists
from src.domain.collections import AccountNotFound
```
