import pathlib

from src.common.keyboard.collections import SYMBOL_FORWARD_SLASH


def current() -> pathlib.Path:
    return pathlib.Path.cwd()


def define(path: str | pathlib.Path | None = None) -> pathlib.Path:
    if not path:
        return current()
    elif isinstance(path, str) and path.startswith(SYMBOL_FORWARD_SLASH):
        return pathlib.Path(path)
    else:
        return current() / path
