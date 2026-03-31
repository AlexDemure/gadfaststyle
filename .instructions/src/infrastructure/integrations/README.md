## Описание

`integrations` описывает внешние сервисные интеграции.

## Правила

- В `integrations` размещай клиентов внешних API и сервисов.
- Клиент оформляй как singleton через `setup.py` и `__init__.py`.
- Если пакет управляет lifecycle, добавляй `start()` и `shutdown()`.
- Публичные объекты экспортируй через `__init__.py`.

## Примеры

```python
from src.infrastructure.integrations.some_api import client
```
