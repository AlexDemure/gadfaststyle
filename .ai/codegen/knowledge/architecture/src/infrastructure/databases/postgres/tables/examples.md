## Эталонная форма

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

