import base64
import typing

from . import json


def encode(data: dict[str, typing.Any]) -> str:
    return base64.urlsafe_b64encode(json.tostring(data).encode()).decode()


def decode(data: str) -> typing.Any:
    return json.fromstring(base64.urlsafe_b64decode(data).decode())
