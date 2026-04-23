import types

from src.application.utils.account import decrypt
from src.decorators.usecases.session import sessionmaker
from src.domain.models import Account
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres.adapters import repositories
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.collections import TokenPurpose


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

    @sessionmaker.read
    async def __call__(self, session: Session, token: str) -> Account:
        self.build(session)

        signature = self.container.security.jwt.decode(token=token, purpose=TokenPurpose.access)

        account = await self.container.repository.account.one(Filter.eq(key="id", value=int(signature.sub)))

        return decrypt(decrypter=self.container.security.encryption.decrypt, account=account)
