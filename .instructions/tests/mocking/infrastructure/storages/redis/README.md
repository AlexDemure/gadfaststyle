## Описание

`mocking/infrastructure/storages/redis` описывает Redis-моки для тестов.

## Правила

- Mock должен повторять публичный контракт Redis-клиента проекта.
- Поведение по умолчанию делай безопасным и детерминированным.
- Не добавляй в mock лишние методы, которых нет у реального клиента.

## Примеры

```python
from tests.mocking.infrastructure.storages.redis import Redis
```
