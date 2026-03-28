# HTTP Public: Schemas

## Что входит в раздел

- `src/entrypoints/http/public/schemas/`

## Базовые правила

- Схемы одного домена группируй в одном модуле, если это уже соответствует текущему стилю.
- Для request используй базовые классы из `src/entrypoints/http/common/schemas`.
- Для response используй `Response`.
- Наследование и базовые public-схемы повторяй по текущему паттерну `public`.
- Имена схем строятся как `<Operation><Entity>`.
- Для search-запросов используй явную структуру `filters`, `sorting`, `pagination`.
- Если ручка работает как легкий справочник и пагинация не нужна, поле `pagination` не добавляй.

## Эталон request/response

```python
import typing

from src.common.formats.utils import field
from src.domain.models import Account
from src.entrypoints.http.common.schemas import Command
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response

from .base import Public


class CreateAccount(Public, Request, Command):
    external_id: str


class CurrentAccount(Public, Response):
    id: int

    @classmethod
    def serialize(cls, account: Account) -> typing.Self:
        return cls(id=field.required(account.id))
```

## Эталон search-схемы

```python
import typing

from pydantic import Field

from src.common.formats.utils import field
from src.common.formats.utils import string
from src.common.locales.collections import Locale
from src.common.typings.validators import Search
from src.common.typings.validators import StrRef
from src.domain.models import City as _City
from src.entrypoints.http.common.schemas import Query
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response
from src.infrastructure.databases.orm.sqlalchemy.collections import Direction

from .base import Public


class SearchCity(Public, Request, Query):
    class SearchCityFilters(Public, Request, Query):
        country_id: StrRef = Field(..., alias="country")
        name: Search | None = None

    class SearchCitySorting(Public, Request, Query):
        field: Locale = Locale.en
        direction: Direction = Direction.asc

    filters: SearchCityFilters
    sorting: SearchCitySorting


class City(Public, Response):
    id: int
    ascii: str
    origin: str
    en: str | None
    ru: str | None
    active: bool | None = None

    @classmethod
    def serialize(cls, model: _City) -> typing.Self:
        return cls(
            id=model.id,
            ascii=string.title(model.ascii),
            origin=string.title(model.origin),
            en=field.safe(string.title, model.en),
            ru=field.safe(string.title, model.ru),
            active=getattr(model, "active", None),
        )
```
