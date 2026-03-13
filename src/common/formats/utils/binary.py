from src.common.formats.collections import ENCODING_UTF
from src.common.keyboard.collections import SYMBOL_EMPTY
from src.common.keyboard.collections import SYMBOL_NEWLINE

from .string import strip


def tostring(string: bytes) -> str:
    return strip(string.decode(ENCODING_UTF).replace(SYMBOL_NEWLINE, SYMBOL_EMPTY))
