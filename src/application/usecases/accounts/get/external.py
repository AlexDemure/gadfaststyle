from src.common.formats.utils import string
from src.domain.collections import AccountBlocked
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption


class Repositories:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption


class Container:
    def __init__(self, repositories: Repositories, security: Security) -> None:
        self.repositories = repositories
        self.security = security


class Usecase:
    def __init__(self, container: Container) -> None:
        self.container = container

    async def __call__(self, external_id: str) -> Account:
        external_id = self.container.security.encryption.encrypt(string.lower(external_id))

        account = await self.container.repositories.account.one(Filter.eq(key="external_id", value=external_id))

        if account.blocked:
            raise AccountBlocked

        return account
