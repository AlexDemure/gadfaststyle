## Описание

`security` описывает security-клиенты.

## Правила

- В `security` размещай runtime-клиенты для шифрования, токенов и другой security-логики.
- Клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные объекты экспортируй через `__init__.py`.

## Примеры

```python
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
```
