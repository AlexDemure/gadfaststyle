## Описание

`postgres/collections/exceptions` описывает исключения Postgres-слоя.

## Правила

- Исключения этого слоя отражают database- и adapter-сбои.
- Не смешивай их с domain-исключениями.
- Каждое исключение описывает один тип ошибки.

## Примеры

```python
class PostgresError(Exception):
    pass
```
