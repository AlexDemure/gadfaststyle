from src.decorators import sessionmaker
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.models import Tokens


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Security:
    def __init__(self) -> None:
        self.encryption = encryption
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

    @sessionmaker.write
    async def __call__(self, session: Session, external_id: str) -> Tokens:
        self.build(session)

        if await self.container.repository.account.exists(
            Filter.eq(
                key="external_id",
                value=self.container.security.encryption.encrypt(external_id.lower()),
            )
        ):
            raise AccountAlreadyExists

        account = await self.container.repository.account.create(
            model=Account.init(
                **Account.encrypt(
                    encrypter=self.container.security.encryption.encrypt,
                    external_id=external_id,
                ),
            )
        )

        tokens = self.container.security.jwt.encode(subject=str(account.id))

        return tokens
