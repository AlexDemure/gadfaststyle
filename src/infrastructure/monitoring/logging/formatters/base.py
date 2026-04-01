import logging
import typing

from src.infrastructure.monitoring.logging.collections import FIELDS_RESERVED
from src.infrastructure.monitoring.logging.mappers import Message
from src.infrastructure.monitoring.logging.parsers import sethidden
from src.infrastructure.monitoring.logging.parsers import setnone


class Formatter(logging.Formatter):
    def __init__(
        self,
        message: list[tuple[str, typing.Callable[[logging.LogRecord], typing.Any]]] | None = None,
        hidden: list[str] | None = None,
        context: typing.Callable[[], dict[str, typing.Any]] | None = None,
    ) -> None:
        super().__init__()
        self.message = message if message else Message
        self.hidden = hidden if hidden else []
        self.context = context if context else lambda: {}

    def enrich(self, record: logging.LogRecord) -> None:
        for field, func in self.message:
            setattr(record, field, func(record))

        for key, value in self.context().items():
            setattr(record, key, value)

        if record.levelno >= logging.WARNING and record.exc_info:
            setattr(record, "stacktrace", self.formatException(record.exc_info))
            setattr(record, "exception", str(record.exc_info[1]))

        if self.hidden:
            for key, value in record.__dict__.items():
                if key not in FIELDS_RESERVED:
                    setattr(record, key, sethidden(value, self.hidden))

        for key, value in record.__dict__.items():
            if key not in FIELDS_RESERVED:
                setattr(record, key, setnone(value))
