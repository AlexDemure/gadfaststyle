## Правила

- В `integrations` размещай клиентов внешних API и сервисов.
- Integration-клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные integration-объекты экспортируй через `__init__.py`.
