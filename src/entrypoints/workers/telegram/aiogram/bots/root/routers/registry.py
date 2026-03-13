from aiogram import Router

from . import callbacks
from . import messages


router = Router()

router.include_router(messages.router)
router.include_router(callbacks.router)
