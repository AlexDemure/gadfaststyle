## Эталонная форма

```python
import typing

from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import select

from src.infrastructure.databases.orm.sqlalchemy.collections import Direction
from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.orm.sqlalchemy.utils import fetchall
from src.infrastructure.databases.orm.sqlalchemy.utils import fetchcount
from src.infrastructure.databases.postgres import tables


class Account(Base[tables.Account]):
    table = tables.Account

    @classmethod
    async def search(
        cls,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[tables.Account], int]:
        statement = select(cls.table)

        if filters.get("id"):
            statement = statement.where(cls.table.id == filters["id"])

        if sorting.get("direction") is Direction.asc:
            statement = statement.order_by(asc(cls.table.created), desc(cls.table.id))
        else:
            statement = statement.order_by(desc(cls.table.created), desc(cls.table.id))

        rows = await fetchall(
            session,
            statement.limit(pagination["limit"]).offset(pagination["offset"]),
        )
        count = await fetchcount(session, statement)

        return rows, count
```

