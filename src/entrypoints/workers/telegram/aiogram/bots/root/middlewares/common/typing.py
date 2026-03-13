import typing

from aiogram import BaseMiddleware


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        await event.bot.send_chat_action(chat_id=event.chat.id, action="typing")
        return await handler(event, data)
