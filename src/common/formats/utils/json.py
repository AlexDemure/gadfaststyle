import base64
import json
import typing

from src.common.formats.encoders import JSONEncoder


def tostring(obj: typing.Any, sort_keys: bool = False, indent: int | None = None, ensure_ascii: bool = False) -> str:
    return json.dumps(obj, cls=JSONEncoder, sort_keys=sort_keys, indent=indent, ensure_ascii=ensure_ascii)


def fromstring(text: str) -> typing.Any:
    return json.loads(text)


def atob(text: str) -> typing.Any:
    return json.loads(base64.urlsafe_b64decode(text + "=="))
