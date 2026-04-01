## Описание

`framework/openapi/handlers` описывает обработчики OpenAPI-генерации.

## Правила

- Каждый handler меняет одну часть OpenAPI-спецификации.
- Handler не должен знать о бизнесовых usecase и конкретных сущностях.
- Изменения спецификации делай явными и локальными.

## Примеры

```python
from src.framework.openapi.handlers import affix
```
