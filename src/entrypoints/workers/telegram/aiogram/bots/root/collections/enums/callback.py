from enum import Enum

from aiogram import F
from aiogram import MagicFilter  # type:ignore


class Callback(str, Enum):
    menu = "menu"

    @property
    def filter(self) -> MagicFilter:
        return F.data == self
