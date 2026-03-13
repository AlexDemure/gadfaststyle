from aiogram import Bot


async def setup(bot: Bot) -> None:
    await bot.set_my_commands([])
