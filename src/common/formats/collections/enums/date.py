import enum


class Format(enum.StrEnum):
    year = "%Y"
    month = "%m"
    month_short = "%b"
    month_full = "%B"
    day = "%d"
    day_short = "%a"
    day_full = "%A"
    hour = "%H"
    minute = "%M"
    second = "%S"
    microsecond = "%f"
    timezone = "%z"

    @classmethod
    def iso(cls) -> str:
        return "{year}-{month}-{day}T{hour}:{minute}:{second}.{microsecond}{timezone}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            microsecond=cls.microsecond.value,
            timezone=cls.timezone.value,
        )

    @classmethod
    def short(cls) -> str:
        return "{year}-{month}-{day}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
        )

    @classmethod
    def full(cls) -> str:
        return "{day_short}, {day} {month_short} {year} {hour}:{minute}:{second}".format(
            day_short=cls.day_short.value,
            day=cls.day.value,
            month_short=cls.month_short.value,
            year=cls.year.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
        )

    @classmethod
    def human(cls) -> str:
        return "{day} {month_full} {year}".format(
            day=cls.day.value,
            month_full=cls.month_full.value,
            year=cls.year.value,
        )

    @classmethod
    def time(cls) -> str:
        return "{hour}:{minute}:{second}".format(
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
        )

    @classmethod
    def us(cls) -> str:
        return "{month}/{day}/{year}".format(
            month=cls.month.value,
            day=cls.day.value,
            year=cls.year.value,
        )

    @classmethod
    def eu(cls) -> str:
        return "{day}/{month}/{year}".format(
            day=cls.day.value,
            month=cls.month.value,
            year=cls.year.value,
        )

    @classmethod
    def rfc2822(cls) -> str:
        return "{day_short}, {day} {month_short} {year} {hour}:{minute}:{second} {timezone}".format(
            day_short=cls.day_short.value,
            day=cls.day.value,
            month_short=cls.month_short.value,
            year=cls.year.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            timezone=cls.timezone.value,
        )

    @classmethod
    def rfc3339(cls) -> str:
        return "{year}-{month}-{day}T{hour}:{minute}:{second}{timezone}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            timezone=cls.timezone.value,
        )
