import types

from src.decorators.usecases.session import sessionmaker
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres.adapters import repositories
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.models import Tokens


class Usecase:
    container: types.SimpleNamespace

    def build(self, session: Session) -> None:
        self.container = types.SimpleNamespace(
            repository=types.SimpleNamespace(
                account=repositories.Account(session),
            ),
            security=types.SimpleNamespace(
                encryption=encryption,
                jwt=jwt,
            ),
        )

    async def validate(self, external_id: str) -> None:
        if await self.container.repository.account.exists(Filter.eq(key="external_id", value=external_id)):
            raise AccountAlreadyExists

    @sessionmaker.write
    async def __call__(self, session: Session, external_id: str) -> Tokens:
        self.build(session)

        encrypted = self.container.security.encryption.encrypt(external_id)

        await self.validate(external_id=encrypted)

        account = await self.container.repository.account.create(model=Account.init(external_id=encrypted))

        return self.container.security.jwt.encode(subject=str(account.id))
