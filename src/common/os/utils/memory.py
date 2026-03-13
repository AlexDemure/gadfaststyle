from src.common.os.collections import KB
from src.common.os.collections import MB


def megabytes(number: int) -> int:
    return number * MB


def kilobytes(number: int) -> int:
    return number * KB
