## Описание

`framework` описывает общий каркас приложения поверх FastAPI и внутренних утилит рантайма.

## Правила

- В `framework` держи только переиспользуемый код рантайма: routing, openapi, background и общие framework-коллекции.
- `framework` не содержит бизнесовых usecase, доменных моделей и предметных HTTP-ручек.
- Общие framework-объекты экспортируй через пакет, если это уже принято в текущем модуле.
- Новый framework-код должен быть пригоден для повторного использования в нескольких участках проекта.

## Примеры

```python
from src.framework.openapi import client
from src.framework.routing.router import Router
```
