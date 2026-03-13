import inspect
import typing

from pydantic import BaseModel
from pydantic import ConfigDict


class Affix(BaseModel):
    __affix__ = ""

    def __init_subclass__(cls, **kwargs: typing.Any):
        super().__init_subclass__(**kwargs)

        prefixes, postfixes = [], []

        for base in inspect.getmro(cls):
            if base in (Affix, BaseModel):
                continue
            affix = getattr(base, "__affix__", None)
            if affix:
                if affix.endswith(":"):
                    if affix[:-1] not in prefixes:
                        prefixes.append(affix[:-1])
                elif affix.startswith(":"):
                    if affix[1:] not in postfixes:
                        postfixes.append(affix[1:])

        if prefixes or postfixes:
            config = dict(cls.model_config)
            config.pop("title", None)
            config["title"] = f"{''.join(prefixes)}{cls.__name__}{''.join(postfixes)}"
            cls.model_config = typing.cast(ConfigDict, config)
