import datetime
import decimal
import enum
import json
import typing

from pydantic import BaseModel


class Encoder(json.JSONEncoder):
    def default(self, obj: typing.Any) -> typing.Any:
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, BaseModel):
            return obj.model_dump()
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)
