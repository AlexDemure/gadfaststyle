from fastapi import Body
from fastapi import Depends
from fastapi import Response
from fastapi import status

from src.application.usecases.accounts.update import Usecase
from src.common.formats.utils import field
from src.domain.collections import AccountAlreadyExists
from src.domain.collections import AccountBlocked
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.entrypoints.http.common.collections import AUTHORIZATION_ERRORS
from src.entrypoints.http.common.deps import account
from src.entrypoints.http.public.deps.accounts.update import dependency
from src.entrypoints.http.public.schemas import UpdateAccount
from src.framework.openapi.utils import errors
from src.framework.routing import APIRouter


router = APIRouter()


@router.patch(
    "/accounts:update",
    description="Account update",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        **errors(
            *AUTHORIZATION_ERRORS,
            AccountNotFound,
            AccountBlocked,
            AccountAlreadyExists,
        ),
    },
)
async def command(
    usecase: Usecase = Depends(dependency),
    _account: Account = Depends(account),
    body: UpdateAccount = Body(...),
) -> None:
    await usecase(account_id=field.required(_account.id), **body.deserialize())
