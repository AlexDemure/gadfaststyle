## Описание

`encryption/collections/exceptions` описывает исключения encryption-слоя.

## Правила

- Исключения должны описывать только ошибки шифрования и дешифрования.
- Не смешивай их с domain- и transport-ошибками.
- Каждое исключение описывает один тип сбоя.

## Примеры

```python
class EncryptionError(Exception):
    pass
```
