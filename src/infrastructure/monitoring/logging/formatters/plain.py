import logging

from src.infrastructure.monitoring.logging.utils import string

from .base import Formatter as _Formatter


class Formatter(_Formatter):
    def format(self, record: logging.LogRecord) -> str:
        self.enrich(record)
        self._style._fmt = "{timestamp} {level} {logger} {message} {{{context}}}".format(
            timestamp=string.wrap("timestamp"),
            level=f"[{string.wrap('level')}]",
            logger=string.wrap("logger"),
            message=string.wrap("message"),
            context=", ".join(
                [
                    f"{key}: {string.wrap(key)}"
                    for key, _ in self.message
                    if key not in {"timestamp", "level", "logger", "message"}
                ]
            ),
        )
        return super().format(record)
