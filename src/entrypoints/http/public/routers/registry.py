from src.framework.routing import APIRouter


router = APIRouter(prefix="/api")

from . import accounts


router.include_router(accounts.router, tags=["Account"])
