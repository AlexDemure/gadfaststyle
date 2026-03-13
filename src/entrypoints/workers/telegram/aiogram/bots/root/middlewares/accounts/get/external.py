import typing

from aiogram import BaseMiddleware

from src.entrypoints.workers.telegram.aiogram.bots.root.services.accounts.get.external import service


class Middleware(BaseMiddleware):
    async def __call__(self, handler: typing.Any, event: typing.Any, data: dict[str, typing.Any]) -> typing.Any:
        if user := data.get("event_from_user"):
            account, blocked = await service(external_id=str(user.id))
            if blocked:
                return None
            data["account"] = account
        return await handler(event, data)
