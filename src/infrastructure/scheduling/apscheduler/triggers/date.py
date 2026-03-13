import datetime
import typing

from apscheduler.triggers.date import DateTrigger


def time(date: datetime.datetime) -> typing.Any:
    return DateTrigger(run_date=date)
