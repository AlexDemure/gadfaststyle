## Описание

`framework/collections/exceptions` описывает framework-исключения.

## Правила

- Ошибки этого слоя должны описывать технические сбои framework-кода.
- Не размещай здесь предметные и транспортные ошибки.
- Каждое исключение описывает один тип framework-сбоя.

## Примеры

```python
class ModuleError(Exception):
    pass
```
