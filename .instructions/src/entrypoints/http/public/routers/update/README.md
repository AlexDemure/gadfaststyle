## Описание

`update` описывает public router для обновления.

## Правила

- Используй `update.py` для mutation-ручек обновления.
- Handler называй `command`.
- Схема запроса явно описывает изменяемые поля.
- Endpoint только вызывает usecase и не делает прикладных проверок.

## Примеры

```python
@router.patch("/accounts:update", response_model=CurrentAccount)
async def command(
    body: UpdateAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> CurrentAccount:
    account = await usecase(**body.deserialize())
    return CurrentAccount.serialize(account)
```
