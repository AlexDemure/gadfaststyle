from . import middlewares
from . import routers
from .bot import bot
from .dispatch import dispatcher


async def run() -> None:
    dispatcher.callback_query.middleware(middlewares.common.error.Middleware())

    dispatcher.message.middleware(middlewares.common.error.Middleware())
    dispatcher.message.middleware(middlewares.common.command.Middleware())
    dispatcher.message.middleware(middlewares.common.typing.Middleware())

    dispatcher.update.middleware(middlewares.common.locale.Middleware())
    dispatcher.update.middleware(middlewares.common.localization.Middleware())
    dispatcher.update.middleware(middlewares.accounts.get.external.Middleware())

    dispatcher.include_router(routers.router)

    await dispatcher.start_polling(bot)
