## Описание

`sqlalchemy/utils` описывает утилиты ORM-слоя.

## Правила

- Утилиты должны быть техническими и переиспользуемыми.
- Не смешивай их с builders, queries и CRUD-реализациями.
- Побочные эффекты делай явными.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import utils
```
