from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.list import Usecase
from src.entrypoints.http.common.schemas import Pagination
from src.entrypoints.http.system.deps.accounts import dependency
from src.entrypoints.http.system.schemas import Accounts
from src.framework.routing import APIRouter


router = APIRouter()


@router.get(
    "/accounts",
    description="Get accounts",
    response_model=Accounts,
    status_code=status.HTTP_200_OK,
)
async def query(usecase: Usecase = Depends(dependency), pagination: Pagination = Depends()) -> Accounts:
    accounts, total = await usecase(**pagination.convert)

    return Accounts.serialize(accounts=accounts, total=total)
