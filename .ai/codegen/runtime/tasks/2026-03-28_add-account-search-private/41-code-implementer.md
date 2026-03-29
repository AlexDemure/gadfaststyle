# Code Implementer Iteration 2

## Reason For Update

Исходная реализация использовала generic `paginated(...)` и собирала builder-объекты в usecase. Для бизнес-ручки `:search` это неверный паттерн.

## Changes

- `src/application/usecases/accounts/search.py`
  - удалена сборка `Filter`, `Sorting`, `Pagination` в usecase
  - `filters`, `sorting`, `pagination` теперь прокидываются в adapter как словари
  - `decrypt` вынесен в отдельный шаг перед `return`
- `src/infrastructure/databases/postgres/adapters/repositories/account.py`
  - добавлен `search(filters, sorting, pagination)`
- `src/infrastructure/databases/postgres/crud/account.py`
  - добавлен entity-specific `search(...)`
  - SQLAlchemy statement собирается вручную под `accounts:search`

## Code Artifacts

### `src/application/usecases/accounts/search.py`

```python
    @sessionmaker.read
    async def __call__(
        self,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[Account], int]:
        self.build(session)

        accounts, total = await self.container.repository.account.search(
            filters=filters,
            sorting=sorting,
            pagination=pagination,
        )

        accounts = [
            account.decrypt(
                decrypter=self.container.security.encryption.decrypt,
                account=_account,
            )
            for _account in accounts
        ]

        return accounts, total
```

### `src/infrastructure/databases/postgres/adapters/repositories/account.py`

```python
    async def search(
        self,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[models.Account], int]:
        rows, total = await self.crud.search(
            session=self.session,
            filters=filters,
            sorting=sorting,
            pagination=pagination,
        )
        return [self.convert(row) for row in rows], total
```

### `src/infrastructure/databases/postgres/crud/account.py`

```python
    @classmethod
    async def search(
        cls,
        session: Session,
        filters: dict[str, typing.Any],
        sorting: dict[str, typing.Any],
        pagination: dict[str, typing.Any],
    ) -> tuple[list[tables.Account], int]:
        statement = select(cls.table)

        if filters.get("id"):
            statement = statement.where(cls.table.id == filters["id"])

        if sorting.get("direction") is Direction.asc:
            statement = statement.order_by(asc(cls.table.created), desc(cls.table.id))
        else:
            statement = statement.order_by(desc(cls.table.created), desc(cls.table.id))

        rows = await fetchall(
            session,
            statement.limit(pagination["limit"]).offset(pagination["offset"]),
        )
        count = await fetchcount(session, statement)

        return rows, count
```

## Checks

### `python3 -m compileall src/application/usecases/accounts src/infrastructure/databases/postgres src/entrypoints/http/system`

Passed.
