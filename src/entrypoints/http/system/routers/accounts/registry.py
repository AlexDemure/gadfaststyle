from src.framework.routing import APIRouter

from . import list


router = APIRouter()

router.include_router(list.router)
