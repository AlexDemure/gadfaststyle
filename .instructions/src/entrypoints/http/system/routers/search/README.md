## Описание

`search` описывает system router для выборки коллекции.

## Правила

- Используй `search.py` для ручек выборки коллекции.
- Handler обычно называй `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, не добавляй ее.
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
