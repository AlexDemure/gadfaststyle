## Описание

`sqlalchemy/builders` описывает сборщики SQLAlchemy-конструкций.

## Правила

- Каждый builder отвечает за один вид конструкции или набора параметров.
- Builder не должен знать о предметной модели.
- Сложную сборку запросов выноси сюда, а не в CRUD-файл.

## Примеры

```python
from src.infrastructure.databases.orm.sqlalchemy import builders
```
