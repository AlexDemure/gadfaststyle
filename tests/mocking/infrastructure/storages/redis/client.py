import datetime
import functools
import typing


class Redis:
    def __init__(self) -> None:
        self.client = None
        self.router = None

    async def start(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def set(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        pass

    async def get(self, _: str) -> dict[str, typing.Any]:
        return {}

    async def delete(self, key: str) -> None:
        pass

    def endpoints(self) -> None:
        pass

    def __call__(
        self,
        namespace: str,
        ttl: datetime.timedelta,
    ) -> typing.Callable[..., typing.Callable[..., typing.Any]]:
        def decorator(func: typing.Any) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
            @functools.wraps(func)
            async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    def invalidate(self, *_: str) -> typing.Callable[..., typing.Callable[..., typing.Any]]:
        def decorator(func: typing.Any) -> typing.Callable[..., typing.Awaitable[typing.Any]]:
            @functools.wraps(func)
            async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                return await func(*args, **kwargs)

            return wrapper

        return decorator
