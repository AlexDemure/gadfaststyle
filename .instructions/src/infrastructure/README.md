## Описание

`infrastructure` описывает инфраструктурный слой.

## Правила

- `infrastructure` изолирует внешние системы и технические реализации.
- Новые пакеты раскладывай по типу интеграции: `databases`, `security`, `integrations`, `storages`, `monitoring`.
- Клиенты с жизненным циклом оформляй явно: `setup.py`, `__init__.py`, при необходимости `start()` и `shutdown()`.
- Конфигурацию добавляй отдельным классом `BaseSettings` и подключай в общий setup.
- Не поднимай инфраструктурные детали в `domain` и `entrypoints`.

## Примеры

```python
from src.infrastructure.security.jwt import jwt
from src.infrastructure.storages.redis import redis
```
