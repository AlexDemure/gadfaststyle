## Описание

`domain` описывает доменный слой.

## Правила

- `domain` не импортирует `entrypoints`, `application`, `tables`, `crud`, adapters и другие инфраструктурные реализации.
- Модели и коллекции домена экспортируй через `src.domain.models` и `src.domain.collections`.
- Публичные импорты собирай в `__init__.py` через явные импорты и `__all__`.
- В `domain` держи только бизнесовые типы, состояния, ошибки и константы.

## Примеры

```python
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
```
