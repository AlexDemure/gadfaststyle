## Описание

`adapters` описывает repository adapters для Postgres.

## Правила

- Usecase работает с repository adapter, а не с CRUD напрямую.
- Adapter связывает CRUD, table, domain model и доменную ошибку.
- Repository adapters одного домена храни в одном файле домена.
- Публичные adapters экспортируй через `__init__.py`.
- Если пакет уже собирает слои через `__init__.py`, импортируй `models`, `tables`, `crud`, `exceptions` через пакет, а не из внутренних файлов.

## Примеры

```python
from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables


class Account(Base[crud.Account, tables.Account, models.Account, exceptions.AccountNotFound]):
    crud = crud.Account
    table = tables.Account
    model = models.Account
    error = exceptions.AccountNotFound
```
