import typing

from aiogram import BaseMiddleware

from src.entrypoints.workers.telegram.aiogram.bots.root.collections import Command


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        if event.text and event.text.startswith("/"):
            allowed = {Command.start, Command.menu}

            command = event.text.split("/")[-1]

            if command not in allowed:
                return None

        return await handler(event, data)
