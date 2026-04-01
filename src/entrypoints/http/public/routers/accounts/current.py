from fastapi import Depends

from src.application.usecases.accounts.current import Usecase
from src.domain.collections import AccountNotFound
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import jwt
from src.entrypoints.http.public.deps.accounts.current import dependency
from src.entrypoints.http.public.schemas import CurrentAccount
from src.framework.openapi.utils.specification import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.get(
    "/accounts:current",
    response_model=CurrentAccount,
    description="Get current account",
    responses=errors(*AUTHORIZATION_ERRORS, AccountNotFound),
)
async def query(
    usecase: Usecase = Depends(dependency),
    token: str = Depends(jwt),
) -> CurrentAccount:
    return CurrentAccount.serialize(await usecase(token=token))
