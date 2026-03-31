from src.decorators import sessionmaker
from src.domain.collections import AccountAlreadyExists
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

    @sessionmaker.write
    async def __call__(self, session: Session, account_id: int, external_id: str) -> None:
        self.build(session)

        account = await self.container.repository.account.one(Filter.eq(key="id", value=account_id))
        encrypted_external_id = self.container.security.encryption.encrypt(external_id.lower())

        if account.external_id != encrypted_external_id and await self.container.repository.account.exists(
            Filter.eq(key="external_id", value=encrypted_external_id)
        ):
            raise AccountAlreadyExists

        await self.container.repository.account.update(
            id=account_id,
            **{
                "external_id": encrypted_external_id,
            },
        )
