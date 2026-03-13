import typing

from apscheduler.triggers.cron import CronTrigger


def everyday(hour: int = 0, minute: int = 0) -> typing.Any:
    return CronTrigger(hour=hour, minute=minute)


def everymonth(day: int = 1, hour: int = 0, minute: int = 0) -> typing.Any:
    return CronTrigger(day=day, hour=hour, minute=minute)


def everyweekday(day: str, hour: int = 0, minute: int = 0) -> typing.Any:
    return CronTrigger(day_of_week=day, hour=hour, minute=minute)
