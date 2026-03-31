## Описание

`delete` описывает system router для удаления.

## Правила

- Используй `delete.py` для ручек удаления.
- Handler обычно называй `command`.
- Endpoint только вызывает usecase и не содержит бизнес-логики.
- Для пустого ответа повторяй соседний паттерн статуса и response class.

## Примеры

```python
@router.delete("/accounts:delete", status_code=status.HTTP_204_NO_CONTENT)
async def command(usecase: Usecase = Depends(dependency), account_id: int = Query(...)) -> None:
    await usecase(account_id=account_id)
```
