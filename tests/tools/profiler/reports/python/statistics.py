import statistics

from tests.tools.profiler.models import Statistics


def generate(durations: list[float]) -> Statistics:
    return Statistics(
        mean=statistics.mean(durations),
        median=statistics.median(durations),
        stdev=statistics.stdev(durations) if len(durations) > 1 else 0.0,
        min=min(durations),
        max=max(durations),
    )
