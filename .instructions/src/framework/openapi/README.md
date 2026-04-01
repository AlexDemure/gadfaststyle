## Описание

`framework/openapi` описывает общий OpenAPI-каркас проекта.

## Правила

- В `openapi` держи только общую генерацию и настройку OpenAPI.
- Константы, handlers, models и utils раскладывай по подпакетам.
- OpenAPI-код не должен содержать бизнесовые ручки и usecase.

## Примеры

```python
from src.framework.openapi import client
```
