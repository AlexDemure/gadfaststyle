from aiogram import Router

from . import root


router = Router()


router.include_router(root.router)
