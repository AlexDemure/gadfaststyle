## Описание

`redis/collections/exceptions` описывает исключения Redis-слоя.

## Правила

- Исключения должны описывать только ошибки Redis-клиента и его контракта.
- Не смешивай их с domain- и transport-ошибками.
- Каждое исключение описывает один тип Redis-сбоя.

## Примеры

```python
class RedisError(Exception):
    pass
```
