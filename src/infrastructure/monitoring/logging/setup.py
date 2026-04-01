import logging
import logging.config
import sys
import typing

from src.common.formats.utils import modules
from src.configuration import settings
from src.infrastructure.monitoring.logging.formatters import JSONFormatter
from src.infrastructure.monitoring.logging.formatters import PlainFormatter
from src.infrastructure.monitoring.logging.models import Logger


def setup(*loggers: Logger) -> None:
    if not settings.LOGGING:
        return

    config: dict[str, typing.Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {},
        "loggers": {},
        "root": {},
    }

    for logger in loggers:
        formatter: type[PlainFormatter] | type[JSONFormatter] = PlainFormatter
        formattername = "plain"

        if logger.module:
            formattername = modules.define(logger.module)
            if formattername == "json":
                formatter = JSONFormatter

        if formattername not in config["formatters"]:
            config["formatters"][formattername] = {"()": formatter, **logger.kwargs}

        config["handlers"][logger.id] = {
            "class": "logging.StreamHandler",
            "stream": logger.stream or sys.stdout,
            "formatter": formattername,
        }

        if logger.name == "root":
            config["root"] = {
                "handlers": [logger.id],
                "level": logger.level,
            }
        else:
            config["loggers"][logger.name] = {
                "handlers": [logger.id],
                "level": logger.level,
                "propagate": False,
            }

    logging.config.dictConfig(config)


setup(Logger("root", logging.INFO, None, sys.stdout))

logger = logging.getLogger()
