## Описание

`delete` описывает public router для удаления.

## Правила

- Используй `delete.py` для ручек удаления.
- Handler и статус ответа повторяй по принятому паттерну домена.
- Endpoint только вызывает usecase и не содержит бизнес-логики.
- Для пустого ответа используй `Response` и `HTTP_204_NO_CONTENT`, если это уже принято рядом.

## Примеры

```python
@router.delete("/accounts:delete", status_code=status.HTTP_204_NO_CONTENT)
async def query(usecase: Usecase = Depends(dependency), account: Account = Depends(current)) -> None:
    await usecase(account_id=field.required(account.id))
```
