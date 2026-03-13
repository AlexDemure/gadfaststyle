from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message

from src.entrypoints.workers.telegram.aiogram.bots.root import keyboards
from src.entrypoints.workers.telegram.aiogram.bots.root.collections import Command


router = Router()


@router.message(Command.start())
async def handler(message: Message) -> None:
    await message.delete()

    keyboard = keyboards.start.root.keyboard()

    await message.answer(text="Start", reply_markup=keyboard, parse_mode=ParseMode.HTML)
