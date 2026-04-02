import types

from src.decorators.usecases.session import sessionmaker
from src.domain.collections import AccountNotFound
from src.infrastructure.databases.orm.sqlalchemy.collections import Operator
from src.infrastructure.databases.orm.sqlalchemy.models import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres.adapters.repositories import Account as AccountRepository
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.collections import TokenInvalid
from src.infrastructure.security.jwt.collections import TokenPurpose


class Usecase:
    def __init__(self) -> None:
        self.container: types.SimpleNamespace | None = None

    def build(self, session: Session) -> None:
        self.container = types.SimpleNamespace(
            repository=types.SimpleNamespace(
                account=AccountRepository(session),
            ),
            security=types.SimpleNamespace(
                jwt=jwt,
            ),
        )

    async def validate(self, token: str) -> int:
        if not self.container:
            raise ValueError("Container is not initialized")

        signature = self.container.security.jwt.decode(token=token, purpose=TokenPurpose.access)

        try:
            return int(signature.sub)
        except ValueError as error:
            raise TokenInvalid from error

    @sessionmaker.write
    async def __call__(self, session: Session, token: str) -> None:
        self.build(session)

        if not self.container:
            raise ValueError("Container is not initialized")

        account_id = await self.validate(token=token)

        filter_ = Filter(
            key="id",
            value=account_id,
            operator=Operator.eq,
        )

        await self.container.repository.account.one(filter_)

        await self.container.repository.account.delete(filter_)
