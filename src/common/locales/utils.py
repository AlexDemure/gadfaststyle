import langcodes

from src.common.locales.collections import Locale


def getlocale(value: str) -> Locale:
    language = value.split(",")[0].split(";")[0].strip()

    matched = langcodes.closest_supported_match(language, tuple(locale.value for locale in Locale))

    return Locale(matched) if matched else Locale.en
