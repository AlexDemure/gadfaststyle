## Эталонная форма

```python
from src.application.utils.account import decrypt
from src.common.formats.utils import string
from src.decorators import sessionmaker
from src.domain.collections import AccountBlocked
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
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
    async def __call__(self, session: Session, external_id: str) -> Account:
        self.build(session)

        external_id = self.container.security.encryption.encrypt(string.lower(external_id))

        account = await self.container.repository.account.one(Filter.eq(key="external_id", value=external_id))

        if account.blocked:
            raise AccountBlocked

        account = decrypt(
            decrypter=self.container.security.encryption.decrypt,
            account=account,
        )

        return account
```
