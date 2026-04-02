from src.framework.routing import APIRouter

from .create import router as create
from .current import router as current
from .delete import router as delete


router = APIRouter()

router.include_router(create)
router.include_router(current)
router.include_router(delete)
