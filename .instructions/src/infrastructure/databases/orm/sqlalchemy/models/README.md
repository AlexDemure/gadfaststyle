## Описание

`sqlalchemy/models` описывает общие SQLAlchemy-модели и базы.

## Правила

- Здесь держи только технические ORM-модели и базовые классы.
- Предметные table-модели не размещай в этом пакете.
- Публичные модели экспортируй через пакет.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import models
```
