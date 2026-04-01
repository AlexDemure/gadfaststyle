## Описание

`routers` описывает public endpoints.

## Правила

- В каждом файле операции создавай `router = APIRouter()`.
- Не объединяй несколько операций в один router-файл.
- Mutation-обработчик называй `command`, read-обработчик называй `query`, если рядом уже не принят другой паттерн.
- В декораторе ручки всегда указывай `description`.
- Endpoint принимает схему, вызывает usecase и не знает о БД и инфраструктуре напрямую.
- Формат URL должен повторять уже используемый паттерн контура.

## Примеры

```python
router = APIRouter()


@router.post("/accounts:create", description="Создать аккаунт.")
async def command(...) -> Tokens:
    ...
```
