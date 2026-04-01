## Описание

`sqlalchemy/tables` описывает общие table-базы ORM-слоя.

## Правила

- Здесь держи только общие table-базы и mixin-структуры.
- Предметные таблицы размещай в конкретной database-реализации.
- Базовые таблицы не должны содержать бизнесовую семантику.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import tables
```
