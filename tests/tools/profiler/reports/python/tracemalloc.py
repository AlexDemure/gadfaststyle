import tracemalloc

from tests.tools.profiler.models import Allocation


def generate() -> Allocation:
    current, peak = tracemalloc.get_traced_memory()
    return Allocation(current=current, peak=peak)
