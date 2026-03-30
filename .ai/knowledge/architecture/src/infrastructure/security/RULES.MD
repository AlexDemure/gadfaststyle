## Правила

- В `security` размещай runtime-клиенты для шифрования, токенов и другой security-логики.
- Security-клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные security-объекты экспортируй через `__init__.py`.
