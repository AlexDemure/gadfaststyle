## Описание

`exceptions` описывает доменные исключения.

## Правила

- Исключения домена храни в отдельных файлах по сущности или домену.
- Имена строй от сущности и сценария: `AccountNotFound`, `AccountAlreadyExists`.
- Наследование ошибок повторяй по уже принятому базовому типу.
- Публичные исключения экспортируй через `exceptions/__init__.py` и `collections/__init__.py`.

## Примеры

```python
from src.common.http.collections import HTTPError


class AccountNotFound(HTTPError): ...


class AccountBlocked(HTTPError): ...
```
