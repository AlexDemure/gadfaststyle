from src.framework.routing import APIRouter

from . import public
from . import system


router = APIRouter()

router.include_router(public.router)
router.include_router(system.router)
