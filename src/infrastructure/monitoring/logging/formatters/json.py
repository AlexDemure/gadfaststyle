import logging

from src.common.formats.utils import json
from src.infrastructure.monitoring.logging.collections import FIELDS_RESERVED

from .base import Formatter as _Formatter


class Formatter(_Formatter):
    def format(self, record: logging.LogRecord) -> str:
        self.enrich(record)

        root = {field: getattr(record, field) for field, _ in self.message}

        context = {
            key: value
            for key, value in record.__dict__.items()
            if key not in root.keys() and key not in FIELDS_RESERVED
        }

        if context:
            root["context"] = context

        return json.tostring(root)
