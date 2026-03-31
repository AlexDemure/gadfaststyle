## Описание

`public` описывает публичный HTTP-контур.

## Правила

- Новый домен раскладывай по пакетам `routers/<domain>/`, `deps/<domain>/`, `schemas/`.
- Домен подключай через `registry.py`.
- Если после удаления функциональности пакет пустеет, удаляй пустые папки и обновляй `registry.py`.
- Публичный контур не должен содержать внутренние system-only детали.

## Примеры

```python
from src.entrypoints.http.public.registry import registry
```
