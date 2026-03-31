## Описание

`http` описывает HTTP entrypoint.

## Правила

- HTTP-код разделяй по контурам `common`, `public`, `system`.
- Новый домен раскладывай по пакетам `routers`, `deps`, `schemas`.
- Для новых выборок используй `search`, а не `list`.
- Endpoint принимает схему, вызывает usecase и не работает с БД напрямую.

## Примеры

```python
from src.entrypoints.http.public import schemas
from src.entrypoints.http.public.deps.accounts.create import dependency
```
