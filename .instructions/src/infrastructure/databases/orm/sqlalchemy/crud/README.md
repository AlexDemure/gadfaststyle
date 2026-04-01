## Описание

`sqlalchemy/crud` описывает общую CRUD-базу ORM-слоя.

## Правила

- Здесь держи только общие CRUD-абстракции и базовые операции.
- Предметные CRUD-реализации размещай уже в конкретной database-реализации.
- CRUD возвращает technical data, а не domain-модели.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import crud
```
