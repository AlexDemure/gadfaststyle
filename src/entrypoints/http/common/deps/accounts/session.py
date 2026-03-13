from fastapi import Depends

from src.application.usecases.accounts.get.jwt import Container
from src.application.usecases.accounts.get.jwt import Repositories
from src.application.usecases.accounts.get.jwt import Security
from src.application.usecases.accounts.get.jwt import Usecase
from src.domain.models import Account
from src.entrypoints.http.common.deps.database import read
from src.entrypoints.http.common.deps.security import jwt
from src.infrastructure.databases.orm.sqlalchemy.session import Session


async def dependency(
    session: Session = Depends(read),
    token: str = Depends(jwt),
) -> Account:
    usecase = Usecase(container=Container(repositories=Repositories(session), security=Security()))
    return await usecase(token)
