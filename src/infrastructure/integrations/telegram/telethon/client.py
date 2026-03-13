import contextlib
import io
import typing

from telethon import TelegramClient
from telethon.sessions import StringSession

from src.configuration import settings
from src.infrastructure.storages.redis import Redis

from .collections import ClientDisabled


class Client:
    session: str
    storage: Redis

    @classmethod
    @contextlib.asynccontextmanager
    async def manager(cls, commit: bool = False, disconnect: bool = True) -> typing.AsyncGenerator[typing.Any, None]:
        if not settings.TELEGRAM:
            raise ClientDisabled

        session = await cls.storage.get(cls.session)

        client = TelegramClient(
            StringSession(session.get(cls.session)),
            settings.TELEGRAM_ACCOUNT_API_ID,
            settings.TELEGRAM_ACCOUNT_API_HASH,
        )

        if not client.is_connected():
            await client.connect()

        yield client

        if commit:
            if hasattr(client, "session"):
                await cls.storage.set(cls.session, client.session.save())

        if disconnect:
            await client.disconnect()

    @classmethod
    async def info(cls) -> typing.Any | None:
        async with cls.manager() as session:
            return await session.get_me()

    @classmethod
    async def message(cls, entity: typing.Any, message: str) -> None:
        async with cls.manager() as session:
            await session.send_message(entity=entity, message=message, parse_mode="html")

    @classmethod
    async def post(cls, entity: typing.Any, file: io.BytesIO, message: str) -> None:
        async with cls.manager() as session:
            await session.send_file(entity=entity, file=file, caption=message, force_document=False, parse_mode="html")


class Bot(Client):
    session = "telegram:session:bot"

    @classmethod
    async def signin(cls, token: str) -> None:
        async with cls.manager(commit=True) as session:
            await session.sign_in(bot_token=token)


class Telethon:
    bot: Bot

    @classmethod
    async def start(cls, storage: Redis) -> None:
        if not settings.TELEGRAM:
            return

        Bot.storage = storage

        cls.bot = Bot()

        await cls.bot.signin(token=settings.TELEGRAM_BOT_TOKEN)

    @classmethod
    async def shutdown(cls) -> None: ...
