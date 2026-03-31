## Описание

`create` описывает system router для создания.

## Правила

- Используй `create.py` для mutation-ручек создания.
- Handler обычно называй `command`.
- Статус, тело ответа и ошибки повторяй по принятому паттерну `system`.
- Endpoint только вызывает usecase.

## Примеры

```python
@router.post("/accounts:create", response_model=Account)
async def command(
    body: CreateAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Account:
    return Account.serialize(await usecase(**body.deserialize()))
```
