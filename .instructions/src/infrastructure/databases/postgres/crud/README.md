## Описание

`crud` описывает entity-specific CRUD для Postgres.

## Правила

- CRUD работает на уровне table и SQLAlchemy statement.
- Entity-specific запросы вроде `search(...)` собирай в CRUD.
- Возвращай table rows и технические результаты, а не доменные модели.
- CRUD одного домена храни в одном файле домена.
- Публичные CRUD-классы экспортируй через `crud/__init__.py`.

## Примеры

```python
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
        ...
```
