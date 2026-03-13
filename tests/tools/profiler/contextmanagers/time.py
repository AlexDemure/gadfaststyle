import contextlib
import time
import typing


@contextlib.contextmanager
def timer() -> typing.Generator[typing.Callable[[], float], typing.Any, None]:
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start
