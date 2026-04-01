import functools
import typing

from src.infrastructure.databases.postgres import postgres


Callable = typing.Callable[..., typing.Awaitable[typing.Any]]


class SessionMaker:
    def write(self, function: Callable) -> Callable:
        @functools.wraps(function)
        async def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            async with postgres.orm.write() as database_session:
                return await function(self, database_session, *args, **kwargs)

        return wrapper

    def read(self, function: Callable) -> Callable:
        @functools.wraps(function)
        async def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            async with postgres.orm.read() as database_session:
                return await function(self, database_session, *args, **kwargs)

        return wrapper


sessionmaker = SessionMaker()
