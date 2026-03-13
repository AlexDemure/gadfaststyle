from pydantic import BaseModel

from tests.tools.profiler.models.reports.extensions.sqlalchemy import SqlalchemyQuery
from tests.tools.profiler.models.reports.python.garbage import GarbageCollector
from tests.tools.profiler.models.reports.python.tracemalloc import Allocation


class SqlalchemyProfiling(BaseModel):
    query: SqlalchemyQuery
    allocation: Allocation
    garbage: GarbageCollector
