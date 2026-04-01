## Описание

`framework/routing` описывает общий routing-каркас проекта.

## Правила

- В `routing` держи общие router-абстракции и базовые коллекции.
- Routing-код не должен содержать предметные HTTP-ручки.
- Общие enum и наборы значений раскладывай в `collections/`.

## Примеры

```python
from src.framework.routing.router import Router
```
