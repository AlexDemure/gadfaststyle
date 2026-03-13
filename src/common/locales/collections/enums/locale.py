import enum

from src.common.locales.collections.const.region import REGION_CIS


class Locale(enum.StrEnum):
    en = "en"
    ru = "ru"

    @classmethod
    def get(cls, locale: str) -> "Locale":
        return cls.ru if locale in REGION_CIS else cls.en
