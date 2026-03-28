# HTTP Public: Routers

## Что входит в раздел

- `src/entrypoints/http/public/routers/`
- `src/entrypoints/http/public/routers/registry.py`

## Базовые правила

- В каждом файле операции создается `router = APIRouter()`.
- Не объединяй несколько операций в один router-файл.
- Обработчик обычно называется `command` для mutation и `query` для search-ручек.
- Endpoint ничего не знает о БД и инфраструктуре напрямую, он только принимает схему и вызывает usecase.
- Не придумывай новый формат URL, если текущий домен использует `"/accounts:create"`.
- Если добавляется новый домен, подключи его через `registry.py`.

## Навигация по операциям

- `.ai/architecture/src/http/public/routers/operations/create.md`
- `.ai/architecture/src/http/public/routers/operations/delete.md`
- `.ai/architecture/src/http/public/routers/operations/update.md`
- `.ai/architecture/src/http/public/routers/operations/search.md`
- `.ai/architecture/src/http/public/routers/operations/get.md`

## Эталон формы

```python
from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.create import Usecase
from src.domain.collections import AccountAlreadyExists
from src.entrypoints.http.public.deps.accounts.create import dependency
from src.entrypoints.http.public.schemas import CreateAccount
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter
from src.infrastructure.security.jwt.models import Tokens


router = APIRouter()


@router.post(
    "/accounts:create",
    description="Account create",
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED,
    responses=errors(AccountAlreadyExists),
)
async def command(usecase: Usecase = Depends(dependency), body: CreateAccount = Body(...)) -> Tokens:
    return await usecase(**body.deserialize())
```
