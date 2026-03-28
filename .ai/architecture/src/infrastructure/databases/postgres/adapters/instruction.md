# Infrastructure Databases Postgres: Adapters

## Что входит в раздел

- `src/infrastructure/databases/postgres/adapters/`
- `src/infrastructure/databases/postgres/adapters/repositories/`

## Базовые правила

- Usecase должен работать с repository adapter, а не с CRUD напрямую, если домен уже следует этой форме.
- Для каждой сущности создавай отдельный repository adapter.
- Adapter связывает CRUD, table, domain model и доменную ошибку `NotFound`.
- Для бизнес-ручек `:search` добавляй в adapter отдельный метод `search(filters, sorting, pagination)`, который принимает сырые словари из usecase и делегирует их в CRUD.
- Не переноси в adapter бизнес-логику usecase.

## Эталон

```python
from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables

from .base import Base


class Account(Base[crud.Account, tables.Account, models.Account, exceptions.AccountNotFound]):
    crud = crud.Account
    table = tables.Account
    model = models.Account
    error = exceptions.AccountNotFound
```
