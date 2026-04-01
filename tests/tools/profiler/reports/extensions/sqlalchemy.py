from tests.tools.profiler.models import PostgresExplain
from tests.tools.profiler.models import SqlalchemyQuery
from tests.tools.profiler.models import Statistics


def generate(
    sql: tuple[Statistics, Statistics, Statistics],
    orm: tuple[Statistics, Statistics, Statistics],
    explains: list[PostgresExplain],
) -> SqlalchemyQuery:
    return SqlalchemyQuery(
        sql=SqlalchemyQuery.SqlalchemyQueryDetail(execute=sql[0], fetch=sql[1], scalar=sql[2]),
        orm=SqlalchemyQuery.SqlalchemyQueryDetail(execute=orm[0], fetch=orm[1], scalar=orm[2]),
        explains=explains,
    )
