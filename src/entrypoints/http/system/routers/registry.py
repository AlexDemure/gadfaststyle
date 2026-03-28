from src.framework.routing import APIRouter
from fastapi import Depends

from src.entrypoints.http.common.deps import basic

from . import accounts


router = APIRouter(prefix="/api/-")


router.include_router(accounts.router, tags=["Accounts"], dependencies=[Depends(basic)])
