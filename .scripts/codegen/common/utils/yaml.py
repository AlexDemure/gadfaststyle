import pathlib
import typing

import yaml


def load(path: pathlib.Path) -> dict[str, typing.Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return typing.cast(dict[str, typing.Any], data or {})
