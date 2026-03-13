from fastapi import Depends

from src.application.usecases.accounts.delete import Container
from src.application.usecases.accounts.delete import Repositories
from src.application.usecases.accounts.delete import Usecase
from src.entrypoints.http.common.deps import write
from src.infrastructure.databases.orm.sqlalchemy.session import Session


def dependency(session: Session = Depends(write)) -> Usecase:
    return Usecase(container=Container(repositories=Repositories(session)))
