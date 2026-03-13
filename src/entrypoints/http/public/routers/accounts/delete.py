from fastapi import Depends
from fastapi import Response
from fastapi import status

from src.application.usecases.accounts.delete import Usecase
from src.common.formats.utils import field
from src.domain.collections import AccountBlocked
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import account
from src.entrypoints.http.public.deps.accounts.delete import dependency
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.delete(
    "/accounts:delete",
    description="Account delete",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        **errors(
            *AUTHORIZATION_ERRORS,
            AccountNotFound,
            AccountBlocked,
        ),
    },
)
async def query(usecase: Usecase = Depends(dependency), _account: Account = Depends(account)) -> None:
    return await usecase(account_id=field.required(_account.id))
