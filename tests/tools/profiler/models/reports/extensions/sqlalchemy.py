from pydantic import BaseModel

from tests.tools.profiler.models.reports.python.statistics import Statistics

from .postgres import PostgresExplain


class SqlalchemyQuery(BaseModel):
    class SqlalchemyQueryDetail(BaseModel):
        execute: Statistics
        fetch: Statistics
        scalar: Statistics

    sql: SqlalchemyQueryDetail
    orm: SqlalchemyQueryDetail
    explains: list[PostgresExplain]
