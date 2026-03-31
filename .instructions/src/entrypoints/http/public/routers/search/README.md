## Описание

`search` описывает public router для выборки коллекции.

## Правила

- Используй `search.py` для ручек выборки коллекции.
- Handler называй `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, поле `pagination` не добавляй.
- Endpoint только вызывает `usecase(**body.deserialize())`.

## Примеры

```python
@router.post("/accounts:search", response_model=Accounts)
async def query(
    body: SearchAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Accounts:
    accounts, total = await usecase(**body.deserialize())
    return Accounts.serialize(accounts=accounts, total=total)
```
