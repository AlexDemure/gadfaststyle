from src.framework.routing import APIRouter

from . import accounts


router = APIRouter(prefix="/api")


router.include_router(accounts.router, tags=["Accounts"])
