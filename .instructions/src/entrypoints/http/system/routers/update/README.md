## Описание

`update` описывает system router для обновления.

## Правила

- Используй `update.py` для mutation-ручек обновления.
- Handler обычно называй `command`.
- Схема запроса явно описывает изменяемые поля.
- Endpoint только вызывает usecase.

## Примеры

```python
@router.patch("/accounts:update", response_model=Account)
async def command(
    body: UpdateAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Account:
    return Account.serialize(await usecase(**body.deserialize()))
```
