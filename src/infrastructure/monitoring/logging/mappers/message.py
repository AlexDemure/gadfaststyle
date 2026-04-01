import datetime
import logging
import os
import typing

from src.common.formats.utils import date


Mapper: list[tuple[str, typing.Callable[[logging.LogRecord], typing.Any]]] = [
    (
        "timestamp",
        lambda record: date.iso(datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc)),
    ),
    ("level", lambda record: record.levelname),
    ("logger", lambda record: record.name),
    ("message", lambda record: record.getMessage()),
    ("trace_id", lambda record: getattr(record, "trace_id", None)),
    ("span_id", lambda record: getattr(record, "span_id", None)),
    ("user_id", lambda record: getattr(record, "user_id", None)),
    ("request_id", lambda record: getattr(record, "request_id", None)),
    ("url", lambda record: getattr(record, "url", None)),
    ("location", lambda record: f"{record.pathname}:{record.funcName}:{record.lineno}"),
    ("elapsed", lambda record: getattr(record, "elapsed", None)),
    ("ip", lambda record: getattr(record, "ip", None)),
    ("debug", lambda record: getattr(record, "debug", None)),
    ("service", lambda record: os.getenv("SERVICE", None)),
    ("environment", lambda record: os.getenv("ENVIRONMENT", None)),
    ("version", lambda record: os.getenv("VERSION", None)),
    ("pod", lambda record: os.getenv("POD")),
    ("namespace", lambda record: os.getenv("NAMESPACE")),
    ("container", lambda record: os.getenv("CONTAINER")),
    ("process", lambda record: record.process),
    ("thread", lambda record: record.thread),
    ("stacktrace", lambda record: getattr(record, "stacktrace", None)),
    ("exception", lambda record: getattr(record, "exception", None)),
]
