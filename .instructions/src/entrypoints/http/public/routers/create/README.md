## Описание

`create` описывает public router для создания.

## Правила

- Используй `create.py` для mutation-ручек создания.
- Handler называй `command`.
- Обычно используй `Body(...)`, `Depends(dependency)` и `status.HTTP_201_CREATED`.
- Ошибки домена подключай через `responses=errors(...)`, если это уже принято рядом.
- Endpoint только вызывает `usecase(**body.deserialize())`.

## Примеры

```python
@router.post("/accounts:create", status_code=status.HTTP_201_CREATED)
async def command(
    usecase: Usecase = Depends(dependency),
    body: CreateAccount = Body(...),
) -> Tokens:
    return await usecase(**body.deserialize())
```
