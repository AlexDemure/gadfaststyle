import types

from src.decorators.usecases.session import sessionmaker
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres.adapters import repositories
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
                jwt=jwt,
            ),
        )

    @sessionmaker.write
    async def __call__(self, session: Session, token: str) -> None:
        self.build(session)

        signature = self.container.security.jwt.decode(token=token, purpose=TokenPurpose.access)

        await self.container.repository.account.delete(Filter.eq(key="id", value=int(signature.sub)))
