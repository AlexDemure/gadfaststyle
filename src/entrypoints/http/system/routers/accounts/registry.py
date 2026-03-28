from src.framework.routing import APIRouter

from . import search


router = APIRouter()

router.include_router(search.router)
