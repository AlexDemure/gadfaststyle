import asyncio
import logging
import signal
import traceback
import types

from .handles import Signal


logger = logging.getLogger("asyncio.detector")


class Detector:
    def __init__(self, timeout: int = 30) -> None:
        self._timeout = timeout
        self._original_handle_class: type[asyncio.Handle] | None = None

    def start(self) -> None:
        if self._original_handle_class is not None:
            return
        Signal._timeout = self._timeout
        self._original_handle_class = asyncio.Handle
        setattr(asyncio.events, "Handle", Signal)
        signal.signal(signal.SIGALRM, self._message)

    def shutdown(self) -> None:
        if self._original_handle_class:
            setattr(asyncio.events, "Handle", self._original_handle_class)
            self._original_handle_class = None
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

    def _message(self, _: int, frame: types.FrameType | None) -> None:
        stack = [stack for stack in reversed(traceback.extract_stack(frame))][0]
        func, file, lineno, code = stack.name, stack.filename, stack.lineno, stack.line.strip() if stack.line else ""
        logger.critical(
            f"Event loop is blocked for {self._timeout} sec in location {file}:{lineno} in {func}() → {code}"
        )
