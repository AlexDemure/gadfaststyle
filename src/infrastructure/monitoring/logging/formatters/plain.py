import logging

from src.infrastructure.monitoring.logging.utils import string

from .base import Formatter as _Formatter


class Formatter(_Formatter):
    def format(self, record: logging.LogRecord) -> str:
        self.enrich(record)
        context = ", ".join(
            [
                f"{key}: {string.wrap(key)}"
                for key, _ in self.message
                if key not in {"timestamp", "level", "logger", "message"}
            ]
        )
        self._style._fmt = " ".join(
            [
                string.wrap("timestamp"),
                f"[{string.wrap('level')}]",
                string.wrap("logger"),
                string.wrap("message"),
                "{" + context + "}",
            ]
        )
        return super().format(record)
