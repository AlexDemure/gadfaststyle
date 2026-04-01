import datetime

from src.common.formats.collections import Format


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def midnight() -> datetime.datetime:
    return now().replace(hour=0, minute=0, second=0, microsecond=0)


def today() -> datetime.date:
    return now().date()


def previous() -> datetime.datetime:
    return now().replace(day=1) - datetime.timedelta(days=1)


def tostring(date: datetime.datetime, fmt: str) -> str:
    return date.strftime(fmt)


def fromstring(date: str, fmt: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, fmt)


def before(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date < comparison


def after(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date > comparison


def include(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date <= now() <= comparison.date()


def same(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date == comparison


def diff(date: datetime.datetime, comparison: datetime.datetime) -> datetime.timedelta:
    return date - comparison


def age(date: datetime.datetime) -> int:
    return (now() - date).days // 365


def iso(date: datetime.datetime) -> str:
    return tostring(date, Format.iso())


def short(date: datetime.datetime) -> str:
    return tostring(date, Format.short())


def full(date: datetime.datetime) -> str:
    return tostring(date, Format.full())


def human(date: datetime.datetime) -> str:
    return tostring(date, Format.human())


def time(date: datetime.datetime) -> str:
    return tostring(date, Format.time())


def us(date: datetime.datetime) -> str:
    return tostring(date, Format.us())


def eu(date: datetime.datetime) -> str:
    return tostring(date, Format.eu())


def rfc2822(date: datetime.datetime) -> str:
    return tostring(date, Format.rfc2822())


def rfc3339(date: datetime.datetime) -> str:
    return tostring(date, Format.rfc3339())


def start(date: datetime.datetime) -> datetime.datetime:
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def end(date: datetime.datetime) -> datetime.datetime:
    return date.replace(hour=23, minute=59, second=59, microsecond=999999)


def weekend(date: datetime.datetime) -> bool:
    return date.weekday() >= 5


def shift(*, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0) -> datetime.datetime:
    return now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
