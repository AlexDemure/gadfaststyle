## Описание

`storages` описывает storage-клиенты.

## Правила

- В `storages` размещай клиентов для Redis, MinIO, S3 и других хранилищ.
- Клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные объекты экспортируй через `__init__.py`.

## Примеры

```python
from src.infrastructure.storages.redis import redis
```
