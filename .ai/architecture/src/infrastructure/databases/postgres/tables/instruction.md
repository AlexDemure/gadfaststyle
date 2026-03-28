# Infrastructure Databases Postgres: Tables

## Что входит в раздел

- `src/infrastructure/databases/postgres/tables/`

## Базовые правила

- Каждая таблица живет в отдельном файле сущности.
- Имена файлов и классов повторяют имя сущности: `account.py` -> `Account`.
- Таблица описывает только SQLAlchemy-модель persistence-слоя.
- Не смешивай описание таблицы с CRUD, adapter или бизнес-логикой.

## Эталон

```python
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

from src.infrastructure.databases.orm.sqlalchemy.tables import Base
from src.infrastructure.databases.postgres.collections import LENGTH_SMALL_STR


class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)

    external_id = Column(String(length=LENGTH_SMALL_STR), nullable=False, unique=True)

    created = Column(DateTime(timezone=True), nullable=False)
    updated = Column(DateTime(timezone=True), nullable=False)
    blocked = Column(DateTime(timezone=True), nullable=True)
    authorization = Column(DateTime(timezone=True), nullable=True)
```
