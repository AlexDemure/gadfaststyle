# Infrastructure: Storages

## Что входит в раздел

- `src/infrastructure/storages/redis/`

## Назначение

`storages` содержит инфраструктурные клиенты для внешних storage/cache-систем.

## Базовые правила

- Новый клиент должен иметь `client.py` и `setup.py`.
- Если клиент управляет внешним соединением, он должен иметь `start()` и `shutdown()`.
- Подключение клиента должно быть явным в lifecycle приложения.
- Конфигурация клиента должна быть добавлена в `src/configuration/setup.py`.

## Эталон клиента

```python
class Redis:
    def __init__(self) -> None:
        self.client: redis.Redis | None = None
        self.router = APIRouter(tags=["Cache"])
        self.endpoints()

    async def start(self) -> None:
        if not settings.REDIS:
            return

        self.client = redis.from_url(settings.REDIS_HOST, encoding="utf8", decode_responses=True)

        await self.client.ping()  # type:ignore

    async def shutdown(self) -> None:
        if not self.client:
            return

        await self.client.close()
```

## Эталон setup singleton

```python
from .client import Redis


redis = Redis()
```
