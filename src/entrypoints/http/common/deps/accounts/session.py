from fastapi import Depends

from src.application.usecases.accounts.get.jwt import Usecase
from src.domain.models import Account
from src.entrypoints.http.common.deps.security import jwt


async def dependency(token: str = Depends(jwt)) -> Account:
    usecase = Usecase()
    return await usecase(token)
