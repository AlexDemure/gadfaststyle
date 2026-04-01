## Описание

`http/collections` описывает общие HTTP-константы, enum и ошибки.

## Правила

- В `collections` держи только структуры, которые переиспользуются в нескольких HTTP-участках.
- Ошибки и enum разделяй по подпакетам.
- Не размещай здесь схемы, deps и router-код.

## Примеры

```python
from src.common.http.collections import exceptions
```
