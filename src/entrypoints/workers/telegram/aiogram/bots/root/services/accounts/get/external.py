from src.application.usecases.accounts.get.external import Container
from src.application.usecases.accounts.get.external import Repositories
from src.application.usecases.accounts.get.external import Security
from src.application.usecases.accounts.get.external import Usecase
from src.domain.collections import AccountBlocked
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.infrastructure.databases.postgres import postgres


async def service(external_id: str) -> tuple[Account | None, bool]:
    account, blocked = None, False

    async with postgres.orm.read() as session:
        usecase = Usecase(container=Container(repositories=Repositories(session), security=Security()))

        try:
            account = await usecase(external_id=external_id)
        except AccountBlocked:
            blocked = True
        except AccountNotFound:
            ...

    return account, blocked
