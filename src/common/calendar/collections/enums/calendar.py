import enum


class Month(enum.IntEnum):
    january = enum.auto()
    february = enum.auto()
    march = enum.auto()
    april = enum.auto()
    may = enum.auto()
    june = enum.auto()
    july = enum.auto()
    august = enum.auto()
    september = enum.auto()
    october = enum.auto()
    november = enum.auto()
    december = enum.auto()


class Day(enum.StrEnum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"

    @property
    def short(self) -> str:
        mapping: dict[Day, str] = {
            Day.monday: "mon",
            Day.tuesday: "tue",
            Day.wednesday: "wed",
            Day.thursday: "thu",
            Day.friday: "fri",
            Day.saturday: "sat",
            Day.sunday: "sun",
        }
        return mapping[self]
