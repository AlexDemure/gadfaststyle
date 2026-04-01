import types

from src.decorators.usecases.session import sessionmaker
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.collections import Operator
from src.infrastructure.databases.orm.sqlalchemy.models import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres.adapters.repositories import Account as AccountRepository
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.models import Tokens


class Usecase:
    def __init__(self) -> None:
        self.container: types.SimpleNamespace | None = None

    def build(self, session: Session) -> None:
        self.container = types.SimpleNamespace(
            repository=types.SimpleNamespace(
                account=AccountRepository(session),
            ),
            security=types.SimpleNamespace(
                encryption=encryption,
                jwt=jwt,
            ),
        )

    async def validate(self, external_id: str) -> str:
        if not self.container:
            raise ValueError("Container is not initialized")

        encrypted = self.container.security.encryption.encrypt(external_id)

        if await self.container.repository.account.exists(
            Filter(
                key="external_id",
                value=encrypted,
                operator=Operator.eq,
            )
        ):
            raise AccountAlreadyExists

        return encrypted

    @sessionmaker.write
    async def __call__(self, session: Session, external_id: str) -> Tokens:
        self.build(session)

        if not self.container:
            raise ValueError("Container is not initialized")

        encrypted = await self.validate(external_id=external_id)

        account = await self.container.repository.account.create(model=Account.init(external_id=encrypted))

        return self.container.security.jwt.encode(subject=str(account.id))
