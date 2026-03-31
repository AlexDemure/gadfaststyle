from src.framework.routing import APIRouter

from . import create
from . import current
from . import delete
from . import update


router = APIRouter()

router.include_router(current.router)
router.include_router(create.router)
router.include_router(delete.router)
router.include_router(update.router)
