## Эталонная форма

```python
from fastapi import Depends
from fastapi import status

from src.domain.collections import AccountBlocked
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import account
from src.entrypoints.http.public.schemas import CurrentAccount
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.get(
    "/accounts:current",
    description="Get current account",
    response_model=CurrentAccount,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        **errors(
            *AUTHORIZATION_ERRORS,
            AccountNotFound,
            AccountBlocked,
        ),
    },
)
async def query(_account: Account = Depends(account)) -> CurrentAccount:
    return CurrentAccount.serialize(_account)
```

