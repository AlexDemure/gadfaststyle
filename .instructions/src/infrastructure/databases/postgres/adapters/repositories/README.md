## Описание

`postgres/adapters/repositories` описывает repository-адаптеры Postgres.

## Правила

- Каждый repository адаптирует CRUD и tables к domain-контракту.
- Repository возвращает domain-модели, а не table rows.
- Не размещай здесь SQLAlchemy statement-логику.

## Примеры

```python
from src.infrastructure.databases.postgres.adapters import repositories
```
