from fastapi import Body
from fastapi import Depends
from fastapi import status

from src.application.usecases.accounts.search import Usecase
from src.entrypoints.http.system.deps.accounts import dependency
from src.entrypoints.http.system.schemas import Accounts
from src.entrypoints.http.system.schemas import SearchAccount
from src.framework.routing import APIRouter


router = APIRouter()


@router.post(
    "/accounts:search",
    description="Search accounts",
    response_model=Accounts,
    status_code=status.HTTP_200_OK,
)
async def query(
    body: SearchAccount = Body(...),
    usecase: Usecase = Depends(dependency),
) -> Accounts:
    accounts, total = await usecase(**body.deserialize())
    return Accounts.serialize(accounts=accounts, total=total)
