from src.framework.routing import APIRouter

from .create import router as create
from .current import router as current


router = APIRouter()

router.include_router(create)
router.include_router(current)
