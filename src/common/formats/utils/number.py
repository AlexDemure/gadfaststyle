import decimal
import typing


Number = typing.Union[int, float, str, decimal.Decimal]

UNIT = 100


def _decimal(number: Number) -> decimal.Decimal:
    if isinstance(number, decimal.Decimal):
        return number
    return decimal.Decimal(str(number))


def _tounit(number: Number, unit: int = UNIT) -> int:
    return int(_decimal(number) * unit)


def _fromunit(number: Number, unit: int = UNIT) -> decimal.Decimal:
    return decimal.Decimal(number) / unit


def convert(number: Number, current_unit: int, convert_unit: int) -> decimal.Decimal:
    return _fromunit(_tounit(number, current_unit), convert_unit)


def round(number: Number, unit: int = UNIT, rounding: str = decimal.ROUND_HALF_UP) -> decimal.Decimal:
    return _fromunit(_decimal(_tounit(number, unit)).quantize(decimal.Decimal("1"), rounding=rounding), unit)


def add(a: Number, b: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(_tounit(a, unit) + _tounit(b, unit), unit)


def sub(a: Number, b: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(_tounit(a, unit) - _tounit(b, unit), unit)


def mul(a: Number, b: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(_tounit(a, unit) * _tounit(b, unit), unit)


def div(a: Number, b: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(_tounit(a, unit) // _tounit(b, unit), unit)


def split(number: Number, parts: int, unit: int = UNIT) -> list[decimal.Decimal]:
    amount = _tounit(number, unit)
    base = amount // parts
    remainder = amount % parts
    result = [_fromunit(base, unit)] * parts
    for i in range(remainder):
        result[i] = _fromunit(base + 1, unit)
    return result


def compare(a: Number, b: Number, unit: int = UNIT) -> int:
    left = _tounit(a, unit)
    right = _tounit(b, unit)
    return (left > right) - (left < right)


def minvalue(*numbers: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(min(_tounit(number, unit) for number in numbers), unit)


def maxvalue(*numbers: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(max(_tounit(number, unit) for number in numbers), unit)


def sums(*numbers: Number, unit: int = UNIT) -> decimal.Decimal:
    return _fromunit(sum(_tounit(number, unit) for number in numbers), unit)


def area(length: Number, width: Number, unit: int = UNIT) -> decimal.Decimal:
    return mul(length, width, unit)


def volume(length: Number, width: Number, height: Number, unit: int = UNIT) -> decimal.Decimal:
    return mul(mul(length, width, unit), height, unit)
