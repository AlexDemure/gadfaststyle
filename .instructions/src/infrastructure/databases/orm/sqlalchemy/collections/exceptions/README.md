## Описание

`sqlalchemy/collections/exceptions` описывает исключения ORM-слоя.

## Правила

- Ошибки этого слоя отражают технические сбои ORM-кода.
- Не смешивай их с domain- и transport-ошибками.
- Каждое исключение описывает один тип ORM-сбоя.

## Примеры

```python
class ORMError(Exception):
    pass
```
