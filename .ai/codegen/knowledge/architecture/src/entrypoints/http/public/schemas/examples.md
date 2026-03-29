## Эталонная форма

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

