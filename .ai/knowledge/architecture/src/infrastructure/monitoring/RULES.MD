## Правила

- В `monitoring` размещай Sentry, tracing и другие monitoring-пакеты.
- Monitoring-клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные monitoring-объекты экспортируй через `__init__.py`.
