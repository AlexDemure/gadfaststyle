## Описание

`get` описывает public router для чтения одной сущности.

## Правила

- Используй `get.py` или доменный вариант вроде `current.py`.
- Для чтения одной сущности не используй `search`.
- Handler по имени повторяй по принятому паттерну домена.
- Endpoint только вызывает usecase и сериализует результат, если это требует контракт.

## Примеры

```python
@router.get("/accounts:current", response_model=CurrentAccount)
async def query(account: Account = Depends(current)) -> CurrentAccount:
    return CurrentAccount.serialize(account)
```
