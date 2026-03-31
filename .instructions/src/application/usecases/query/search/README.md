## Описание

`search` описывает чтение коллекции данных.

## Правила

- `search` возвращает коллекцию данных.
- Не дублируй в usecase разбор `filters`, `sorting`, `pagination`, если они уже подготовлены схемой.
- Основную логику поиска собирай в repository adapter и entity-specific CRUD `search(...)`.
- Для новых сценариев не используй `list` как паттерн выборки.
- Если поддерживается пагинация, возвращай `tuple[list[Model], int]`.

## Примеры

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
    return await self.container.repository.account.search(
        filters=filters,
        sorting=sorting,
        pagination=pagination,
    )
```
