## Описание

`sqlalchemy/queries` описывает общие query-утилиты ORM-слоя.

## Правила

- Каждая утилита отвечает за один тип SQLAlchemy-запроса.
- Общую сборку выражений держи здесь, а не в предметном CRUD.
- Query-утилиты не должны знать о domain-логике.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import queries
```
