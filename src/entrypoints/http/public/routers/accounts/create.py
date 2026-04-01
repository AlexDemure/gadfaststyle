from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.create import Usecase
from src.domain.collections import AccountAlreadyExists
from src.entrypoints.http.public.deps.accounts.create import dependency
from src.entrypoints.http.public.schemas import CreateAccount
from src.framework.openapi.utils.specification import errors
from src.framework.routing import APIRouter
from src.infrastructure.security.jwt.models import Tokens


router = APIRouter()


@router.post(
    "/accounts:create",
    status_code=status.HTTP_201_CREATED,
    response_model=Tokens,
    description="Create account",
    responses=errors(AccountAlreadyExists),
)
async def command(
    usecase: Usecase = Depends(dependency),
    body: CreateAccount = Body(...),
) -> Tokens:
    return await usecase(**body.deserialize())
