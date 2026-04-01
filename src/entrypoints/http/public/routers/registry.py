from src.framework.routing import APIRouter

from .accounts import router as accounts


router = APIRouter(prefix="/api")

router.include_router(accounts)
