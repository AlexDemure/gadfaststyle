from aiogram import Bot
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.common.formats.utils import field
from src.entrypoints.workers.telegram.aiogram.bots.root import commands
from src.entrypoints.workers.telegram.aiogram.bots.root import keyboards
from src.entrypoints.workers.telegram.aiogram.bots.root.collections import Callback


router = Router()


@router.callback_query(Callback.menu.filter)
async def callback(query: CallbackQuery, bot: Bot) -> None:
    await query.answer()

    message = field.required(query.message)

    await commands.menu.setup(bot=bot)

    keyboard = keyboards.menu.root.keyboard()

    await message.answer(text="Menu", reply_markup=keyboard, parse_mode=ParseMode.HTML)
