# HTTP Public Router Operation: Search

Используй `search.py` для ручек выборки коллекции данных в `public`.

- Handler называется `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, как у легких справочников, поле `pagination` не добавляй.
- Для сложных выборок оборачивай endpoint декоратором `@redis(...)`, если это соответствует текущему паттерну домена.
- Endpoint только вызывает `usecase(**body.deserialize())`.

Эталон:

```python
from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.cities.search import Usecase
from src.entrypoints.http.common.collections import ACTIVE
from src.entrypoints.http.public.deps.cities.search import dependency
from src.entrypoints.http.public.schemas import Cities
from src.entrypoints.http.public.schemas import SearchCity
from src.framework.routing import APIRouter
from src.infrastructure.storages.redis import redis
from src.infrastructure.storages.redis.collections import Namespace
from src.infrastructure.storages.redis.collections import Operation


router = APIRouter()


@router.post(
    "/cities:search",
    summary=ACTIVE,
    description="Search city",
    status_code=status.HTTP_200_OK,
    response_model=Cities,
)
@redis(operation=Operation.search, namespace=Namespace.cities)
async def query(
    body: SearchCity = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Cities:
    cities = await usecase(**body.deserialize())
    return Cities.serialize(cities)
```
