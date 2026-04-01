## Описание

`entrypoints/http/common/collections/errors` описывает общие ошибки HTTP-entrypoints.

## Правила

- Ошибки должны отражать транспортный уровень и HTTP-контекст.
- Не смешивай здесь domain- и infrastructure-исключения.
- Каждое исключение описывает один тип ошибки ответа.

## Примеры

```python
class Unauthorized(Exception):
    pass
```
