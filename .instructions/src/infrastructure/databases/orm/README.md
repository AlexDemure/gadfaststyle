## Описание

`orm` описывает общий ORM-слой проекта.

## Правила

- В `orm` держи только общую ORM-инфраструктуру без привязки к одной сущности.
- Общие builders, queries, models и utils раскладывай по подпакетам.
- ORM-слой не должен содержать domain-логику.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import builders
```
