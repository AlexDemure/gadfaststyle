# Domain Collections: Exceptions

## Что входит в раздел

- `src/domain/collections/exceptions/`

## Базовые правила

- Исключения домена лежат в отдельном файле сущности или домена.
- Имена исключений строятся от сущности и сценария.
- Наследование повторяй по текущему проектному паттерну, например от `HTTPError`, если это уже принятая форма.
- Если появляется новая сущность, обычно рядом нужен и новый файл исключений по той же схеме.

## Эталон

```python
from src.common.http.collections import HTTPError


class AccountNotFound(HTTPError): ...


class AccountBlocked(HTTPError): ...


class AccountAlreadyExists(HTTPError): ...
```
