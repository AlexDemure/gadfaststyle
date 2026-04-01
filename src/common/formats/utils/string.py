import contextlib
import unicodedata

from src.common.formats.collections import ENCODING_ASCII
from src.common.formats.collections import ENCODING_ERROR_IGNORE
from src.common.formats.collections import REGEXP_NON_ALPHANUMERIC
from src.common.formats.collections import REGEXP_PASCAL_WORDS
from src.common.formats.collections import UNICODE_NORMALIZATION_FORM
from src.common.keyboard.collections import SYMBOL_COMMA
from src.common.keyboard.collections import SYMBOL_DOT
from src.common.keyboard.collections import SYMBOL_EMPTY
from src.common.keyboard.collections import SYMBOL_HYPHEN
from src.common.keyboard.collections import SYMBOL_LOWER_HYPHEN
from src.common.keyboard.collections import SYMBOL_TRUNCATION
from src.common.keyboard.collections import SYMBOL_WHITESPACE


def strip(string: str, clean: bool = True) -> str:
    return string.strip() if clean else string


def normalized(string: str, clean: bool = True) -> str:
    return (
        unicodedata.normalize(UNICODE_NORMALIZATION_FORM, strip(string, clean))
        .encode(ENCODING_ASCII, ENCODING_ERROR_IGNORE)
        .decode(ENCODING_ASCII)
    )


def compact(string: str, clean: bool = True) -> str:
    return SYMBOL_WHITESPACE.join(strip(string, clean).split())


def truncate(string: str, length: int, clean: bool = True) -> str:
    return strip(string, clean)[: length - len(SYMBOL_TRUNCATION)] + SYMBOL_TRUNCATION


def remove(string: str, prefix: str | None = None, suffix: str | None = None, clean: bool = True) -> str:
    string = strip(string, clean)
    if prefix:
        string = string.removeprefix(prefix)
    if suffix:
        string = string.removesuffix(suffix)
    return string


def empty(string: str, clean: bool = True) -> bool:
    return not bool(strip(string, clean))


def number(string: str, clean: bool = True) -> bool:
    with contextlib.suppress(ValueError):
        float(strip(string, clean).replace(SYMBOL_COMMA, SYMBOL_DOT))
        return True
    return False


def count(string: str, clean: bool = True) -> int:
    return len(strip(string, clean))


def lower(string: str, clean: bool = True) -> str:
    return strip(string, clean).lower()


def upper(string: str, clean: bool = True) -> str:
    return strip(string, clean).upper()


def title(string: str, clean: bool = True) -> str:
    return strip(string, clean).title()


def capitalize(string: str, clean: bool = True) -> str:
    return strip(string, clean).capitalize()


def sentence(string: str, clean: bool = True) -> str:
    string = compact(string, clean)
    return string[:1].upper() + string[1:].lower() if string else string


def acronym(string: str, clean: bool = True) -> str:
    words = REGEXP_NON_ALPHANUMERIC.findall(strip(string, clean))
    return SYMBOL_EMPTY.join(word[0].upper() for word in words)


def words(string: str, clean: bool = True) -> list[str]:
    return REGEXP_NON_ALPHANUMERIC.findall(strip(string, clean))


def snake(string: str, clean: bool = True) -> str:
    string = strip(string, clean)

    chunks = REGEXP_NON_ALPHANUMERIC.split(string)
    words = []

    for chunk in chunks:
        if not chunk:
            continue

        chunk_words = REGEXP_PASCAL_WORDS.findall(chunk)
        words.extend(chunk_words)

    return SYMBOL_LOWER_HYPHEN.join(word.lower() for word in words if word)


def camel(string: str, clean: bool = True) -> str:
    string = strip(string, clean)

    chunks = REGEXP_NON_ALPHANUMERIC.split(string)
    words: list[str] = []

    for chunk in chunks:
        if not chunk:
            continue

        chunk_words: list[str] = REGEXP_PASCAL_WORDS.findall(chunk)
        words.extend(chunk_words)

    if not words:
        return ""

    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def pascal(string: str, preserve: bool = True, clean: bool = True) -> str:
    string = strip(string, clean)

    chunks = REGEXP_NON_ALPHANUMERIC.split(string)
    words = []

    for chunk in chunks:
        if not chunk:
            continue

        chunk_words = REGEXP_PASCAL_WORDS.findall(chunk)
        for word in chunk_words:
            if preserve and word.isupper() and len(word) > 1:
                words.append(word)
            else:
                words.append(word.capitalize())

    return SYMBOL_EMPTY.join(words)


def kebab(string: str, clean: bool = True) -> str:
    string = strip(string, clean)

    chunks = REGEXP_NON_ALPHANUMERIC.split(string)
    words = []

    for chunk in chunks:
        if not chunk:
            continue

        chunk_words = REGEXP_PASCAL_WORDS.findall(chunk)
        words.extend(chunk_words)

    return SYMBOL_HYPHEN.join(word.lower() for word in words if word)


def split(string: str, separator: str = SYMBOL_WHITESPACE, clean: bool = True) -> list[str]:
    return strip(string, clean).split(separator)


def join(words: list[str], separator: str = SYMBOL_WHITESPACE, clean: bool = True) -> str:
    return separator.join([strip(word, clean) for word in words])


def splitlines(string: str, clean: bool = True) -> list[str]:
    return strip(string, clean).splitlines()
