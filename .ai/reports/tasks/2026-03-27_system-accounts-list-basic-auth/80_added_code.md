# Added Code

```python
# path: src/application/usecases/accounts/list.py
from src.application.utils import account
from src.decorators import sessionmaker
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Pagination
from src.infrastructure.databases.orm.sqlalchemy.queries import Sorting
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption


class Container:
    def __init__(self, repository: Repository, security: Security) -> None:
        self.repository = repository
        self.security = security


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session), security=Security())

    @sessionmaker.read
    async def __call__(self, session: Session, limit: int, offset: int) -> tuple[list[Account], int]:
        self.build(session)

        accounts, total = await self.container.repository.account.paginated(
            filters=[],
            sorting=[Sorting.desc("created")],
            pagination=Pagination.page(limit=limit, offset=offset),
        )

        return [
            account.decrypt(
                decrypter=self.container.security.encryption.decrypt,
                account=_account,
            )
            for _account in accounts
        ], total
```

```python
# path: src/entrypoints/http/system/routers/accounts/list.py
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.list import Usecase
from src.entrypoints.http.common.schemas import Pagination
from src.entrypoints.http.system.deps.accounts import dependency
from src.entrypoints.http.system.schemas import Accounts
from src.framework.routing import APIRouter


router = APIRouter()


@router.get(
    "/accounts",
    description="Get accounts",
    response_model=Accounts,
    status_code=status.HTTP_200_OK,
)
async def query(usecase: Usecase = Depends(dependency), pagination: Pagination = Depends()) -> Accounts:
    accounts, total = await usecase(**pagination.convert)

    return Accounts.serialize(accounts=accounts, total=total)
```
