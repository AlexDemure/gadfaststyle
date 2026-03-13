from aiogram import Router

from . import start


router = Router()

router.include_router(start.router)
