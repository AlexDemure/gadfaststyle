from enum import Enum

from aiogram.filters import Command as _Command


class Command(str, Enum):
    start = "start"
    menu = "menu"

    def __call__(self) -> _Command:
        return _Command(self.value)
