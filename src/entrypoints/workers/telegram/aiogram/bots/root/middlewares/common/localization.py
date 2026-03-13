import typing

from aiogram import BaseMiddleware

from src.entrypoints.workers.telegram.aiogram.bots.root.localization import localization


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        if locale := data.get("locale"):
            data["localization"] = localization(locale)
        return await handler(event, data)
