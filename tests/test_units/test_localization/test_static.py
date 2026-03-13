import pytest

from src.common.locales.collections import Locale
from src.localization import Localization
from src.localization import localization


class TestLocalizationDictionary:
    def given(self) -> None: ...

    def when(self, locale: Locale) -> Localization:
        return localization(locale)

    def then(self) -> None: ...

    @pytest.mark.asyncio
    @pytest.mark.parametrize("locale", [Locale.en, Locale.ru])
    async def test(self, locale: Locale) -> None:
        self.given()
        self.when(locale)
        self.then()
