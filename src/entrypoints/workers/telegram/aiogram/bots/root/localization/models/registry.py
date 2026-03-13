from pydantic import BaseModel

from .commands import Command
from .common import Common
from .keyboards import Keyboard


class Localization(BaseModel):
    common: Common
    command: Command
    keyboard: Keyboard
