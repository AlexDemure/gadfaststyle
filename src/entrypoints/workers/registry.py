from src.framework.background import background

from .telegram.aiogram import bots


def workers() -> None:
    background.add(bots.root.run)
