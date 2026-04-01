## Описание

`common/http` описывает общие HTTP-типы и вспомогательные структуры.

## Правила

- В `common/http` держи только общие HTTP-объекты без привязки к конкретному router.
- Коллекции ошибок и enum раскладывай в `collections/`.
- Не размещай здесь usecase-логику и transport-specific handlers.

## Примеры

```python
from src.common.http import collections
```
