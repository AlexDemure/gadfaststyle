import gc

from tests.tools.profiler.models import GarbageCollector


def generate() -> GarbageCollector:
    collected, uncollectable, _ = gc.get_count()
    return GarbageCollector(collected=collected, uncollectable=uncollectable)
