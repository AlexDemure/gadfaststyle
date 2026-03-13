import typing

from aiogram import BaseMiddleware

from src.common.locales.collections import Locale


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        if user := data.get("event_from_user"):
            data["locale"] = Locale.get(user.language_code) if user.language_code else Locale.en
        return await handler(event, data)
