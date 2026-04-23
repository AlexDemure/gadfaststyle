import pathlib

from src.common.formats.collections import ENCODING_UTF
from src.common.formats.utils import json
from src.common.locales.collections import Locale

from .models import Localization


def localization(locale: Locale) -> Localization:
    with pathlib.Path(f"src/static/localizations/{locale}.json").open(encoding=ENCODING_UTF) as file:
        return Localization.model_validate(json.fromstring(file.read()))
