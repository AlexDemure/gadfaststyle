import typing

from tests.tools.profiler.models import PostgresExplain


def generate(explains: list[dict[str, typing.Any]]) -> list[PostgresExplain]:
    return [PostgresExplain(**explain) for explain in explains]
