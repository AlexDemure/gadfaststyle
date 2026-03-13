import contextlib
import tracemalloc
import typing


@contextlib.contextmanager
def allocation() -> typing.Generator[None]:
    tracemalloc.start()
    try:
        yield
    finally:
        tracemalloc.stop()
