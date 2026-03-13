import typing

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        try:
            return await handler(event, data)
        except Exception as e:
            if isinstance(event, CallbackQuery):
                await event.answer(str(e), show_alert=True)
            elif isinstance(event, Message):
                await event.answer(str(e), reply_markup=ReplyKeyboardRemove())
