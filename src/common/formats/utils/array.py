import typing


def unique(iterable: typing.Iterable[typing.Any]) -> list[typing.Any]:
    return list(dict.fromkeys(iterable))


def flatten(iterable: typing.Iterable[typing.Any]) -> list[typing.Any]:
    array = []
    for item in iterable:
        if isinstance(item, (list, tuple)):
            array.extend(flatten(item))
        else:
            array.append(item)
    return array


def sort(
    iterable: typing.Iterable[typing.Any],
    key: typing.Any | None = None,
    swap: bool = False,
) -> typing.List[typing.Any]:
    return sorted(iterable, key=key, reverse=swap)


def first(iterable: typing.Iterable[typing.Any]) -> typing.Any:
    return next(iter(iterable))


def last(iterable: typing.Sequence[typing.Any]) -> typing.Any:
    return iterable[-1]


def reverse(iterable: typing.Iterable[typing.Any]) -> list[typing.Any]:
    return list(iterable)[::-1]
