import asyncio
import typing


class Background:
    def __init__(self) -> None:
        self._tasks: list[asyncio.Task[typing.Any]] = []
        self._coroutines: list[typing.Callable[..., typing.Any]] = []

    def add(self, func: typing.Callable[..., typing.Any]) -> None:
        self._coroutines.append(func)

    def start(self) -> None:
        self._tasks = [asyncio.create_task(coro()) for coro in self._coroutines]

    def shutdown(self) -> None:
        for task in self._tasks:
            task.cancel()
