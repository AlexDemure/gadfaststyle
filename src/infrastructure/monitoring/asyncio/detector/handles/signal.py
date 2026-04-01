import asyncio
import signal
import typing


class Handle(asyncio.Handle):
    _timeout: int = 30
    _orig_run: typing.Callable[[asyncio.Handle], None]

    def _run(self) -> None:
        signal.alarm(self._timeout)
        try:
            super()._run()
        finally:
            signal.alarm(0)
