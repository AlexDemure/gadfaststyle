from aiogram import Router

from . import menu


router = Router()

router.include_router(menu.router)
