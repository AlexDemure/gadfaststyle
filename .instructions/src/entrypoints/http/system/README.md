## Описание

`system` описывает внутренний HTTP-контур.

## Правила

- Новый домен раскладывай по пакетам `routers/<domain>/`, `deps/<domain>/`, `schemas/`.
- Домен подключай через `registry.py`.
- Если после удаления функциональности пакет пустеет, удаляй пустые папки и обновляй `registry.py`.
- В `system` допускай внутренние административные сценарии, но не смешивай их с `public`.

## Примеры

```python
from src.entrypoints.http.system.registry import registry
```
