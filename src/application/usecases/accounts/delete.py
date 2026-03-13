from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repositories:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Container:
    def __init__(self, repositories: Repositories) -> None:
        self.repositories = repositories


class Usecase:
    def __init__(self, container: Container) -> None:
        self.container = container

    async def __call__(self, account_id: int) -> None:
        await self.container.repositories.account.delete(Filter.eq(key="id", value=account_id))
