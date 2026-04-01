## Описание

`mocking/infrastructure` описывает mock-объекты инфраструктурного слоя.

## Правила

- Здесь размещай mock-клиенты внешних систем и storage-слоя.
- Mock повторяет публичный контракт реальной зависимости.
- Не добавляй поведение, которого нет у реального клиента.

## Примеры

```python
from tests.mocking.infrastructure.storages.redis import Redis
```
