from fastapi import Depends

from src.application.usecases.accounts.create import Container
from src.application.usecases.accounts.create import Repositories
from src.application.usecases.accounts.create import Security
from src.application.usecases.accounts.create import Usecase
from src.entrypoints.http.common.deps import write
from src.infrastructure.databases.orm.sqlalchemy.session import Session


def dependency(session: Session = Depends(write)) -> Usecase:
    return Usecase(container=Container(repositories=Repositories(session), security=Security()))
