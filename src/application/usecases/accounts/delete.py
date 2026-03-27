from src.decorators import sessionmaker
from src.infrastructure.databases.orm.sqlalchemy.queries import Filter
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Container:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session))

    @sessionmaker.write
    async def __call__(self, session: Session, account_id: int) -> None:
        self.build(session)

        await self.container.repository.account.delete(Filter.eq(key="id", value=account_id))
