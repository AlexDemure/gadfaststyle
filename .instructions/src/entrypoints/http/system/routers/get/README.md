## Описание

`get` описывает system router для чтения одной сущности.

## Правила

- Используй `get.py` или текущий доменный вариант.
- Для чтения одной сущности не используй `search`.
- Handler по имени повторяй по принятому паттерну `system`.
- Endpoint только вызывает usecase и сериализует результат, если это требует контракт.

## Примеры

```python
@router.get("/accounts:get", response_model=Account)
async def query(usecase: Usecase = Depends(dependency), account_id: int = Query(...)) -> Account:
    return Account.serialize(await usecase(account_id=account_id))
```
