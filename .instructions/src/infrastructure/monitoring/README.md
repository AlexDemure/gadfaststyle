## Описание

`monitoring` описывает monitoring-пакеты.

## Правила

- В `monitoring` размещай Sentry, tracing и другие monitoring-клиенты.
- Клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные объекты экспортируй через `__init__.py`.

## Примеры

```python
from src.infrastructure.monitoring.sentry import sentry
```
