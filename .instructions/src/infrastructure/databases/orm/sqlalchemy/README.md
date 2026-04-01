## Описание

`orm/sqlalchemy` описывает общий SQLAlchemy-каркас проекта.

## Правила

- В `sqlalchemy` держи только общие абстракции и утилиты для SQLAlchemy.
- Технические collections, exceptions и enums раскладывай по своим подпакетам.
- Код этого слоя не должен зависеть от предметной сущности.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import queries
```
