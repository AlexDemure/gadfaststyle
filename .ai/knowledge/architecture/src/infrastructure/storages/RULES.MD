## Правила

- В `storages` размещай клиентов для Redis, MinIO, S3 и других хранилищ.
- Storage-клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные storage-объекты экспортируй через `__init__.py`.
