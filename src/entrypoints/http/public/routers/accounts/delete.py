from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.delete import Usecase
from src.domain.collections import AccountNotFound
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import jwt
from src.entrypoints.http.public.deps.accounts.delete import dependency
from src.framework.openapi.utils.specification import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.delete(
    "/accounts:current",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete current account",
    responses=errors(*AUTHORIZATION_ERRORS, AccountNotFound),
)
async def command(
    usecase: Usecase = Depends(dependency),
    token: str = Depends(jwt),
) -> None:
    await usecase(token=token)
