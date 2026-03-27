from src.decorators import sessionmaker
from src.domain.collections import AccountBlocked
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.collections import TokenPurpose


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.jwt = jwt


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
    async def __call__(self, session: Session, token: str) -> Account:
        self.build(session)

        account_id = int((self.container.security.jwt.decode(token, TokenPurpose.access)).sub)

        account = await self.container.repository.account.one(Filter.eq(key="id", value=account_id))

        if account.blocked:
            raise AccountBlocked

        return account
