from src.domain.collections import AccountBlocked
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.collections import TokenPurpose


class Repositories:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.jwt = jwt


class Container:
    def __init__(self, repositories: Repositories, security: Security) -> None:
        self.repositories = repositories
        self.security = security


class Usecase:
    def __init__(self, container: Container) -> None:
        self.container = container

    async def __call__(self, token: str) -> Account:
        account_id = int((self.container.security.jwt.decode(token, TokenPurpose.access)).sub)

        account = await self.container.repositories.account.one(Filter.eq(key="id", value=account_id))

        if account.blocked:
            raise AccountBlocked

        return account
