from src.infrastructure.scheduling.apscheduler import apscheduler


def jobs() -> None:
    if not apscheduler.scheduler:
        return
