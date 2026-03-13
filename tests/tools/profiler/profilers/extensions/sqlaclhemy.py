import asyncio
import typing

from sqlalchemy.dialects.postgresql import dialect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Executable
from sqlalchemy.sql import text

from tests.tools.profiler import contextmanagers
from tests.tools.profiler import models
from tests.tools.profiler import reports


class SqlalchemyProfiler:
    def __init__(self, session: AsyncSession, query: Executable, runs: int = 1, users: int | None = None) -> None:
        self._session = session
        self._orm = query
        self._sql = query.compile(dialect=dialect(), compile_kwargs={"literal_binds": True})  # type:ignore
        self._runs = runs
        self._users = users

    async def tables(self) -> typing.Any:
        return (await self._session.execute(self._orm)).scalars().all()

    async def sql(self) -> tuple[float, float, float]:
        with contextmanagers.timer() as timer:
            rows = await self._session.execute(text(str(self._sql)))
        execute = timer()

        with contextmanagers.timer() as timer:
            rows.fetchall()
        fetch = timer()

        with contextmanagers.timer() as timer:
            rows.scalars().all()
        scalar = timer()

        return execute, fetch, scalar

    async def orm(self) -> tuple[float, float, float]:
        with contextmanagers.timer() as timer:
            rows = await self._session.execute(self._orm)
        execute = timer()

        with contextmanagers.timer() as timer:
            rows.fetchall()
        fetch = timer()

        with contextmanagers.timer() as timer:
            rows.scalars().all()
        scalar = timer()

        return execute, fetch, scalar

    async def once(self) -> tuple[typing.Any, tuple[float, float, float], tuple[float, float, float]]:
        return (
            await self.tables(),
            await self.sql(),
            await self.orm(),
        )

    async def iterate(self) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
        sql, orm = [], []
        for _ in range(self._runs):
            _, _sql, _orm = await self.once()
            sql.append(_sql)
            orm.append(_orm)
        return sql, orm

    async def parallel(self) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
        sql, orm = [], []
        for _ in range(self._runs):
            tasks = [self.once() for _ in range(self._users)]  # type:ignore
            results = await asyncio.gather(*tasks)
            for _, _sql, _orm in results:
                sql.append(_sql)
                orm.append(_orm)
        return sql, orm

    async def explain(self) -> list[dict[str, typing.Any]]:
        return (  # type:ignore
            await self._session.execute(
                text(f"EXPLAIN (ANALYZE, VERBOSE, COSTS, BUFFERS, TIMING, SUMMARY, FORMAT JSON) {self._sql}")
            )
        ).scalar()

    async def analyze(self) -> tuple[typing.Any, models.SqlalchemyProfiling]:  # type:ignore
        with (
            contextmanagers.timer(),
            contextmanagers.allocation(),
        ):
            explains = await self.explain()

            tables, sql, orm = await self.once()

            if self._users:
                sql, orm = await self.parallel()  # type:ignore
            elif self._runs > 1:
                sql, orm = await self.iterate()  # type:ignore
            else:
                sql, orm = [sql], [orm]  # type:ignore

            execute, fetch, scalar = list(zip(*sql))  # type:ignore
            sql = (  # type:ignore
                reports.statistics.generate(list(execute)),
                reports.statistics.generate(list(fetch)),
                reports.statistics.generate(list(scalar)),
            )

            execute, fetch, scalar = list(zip(*orm))  # type:ignore
            orm = (  # type:ignore
                reports.statistics.generate(list(execute)),
                reports.statistics.generate(list(fetch)),
                reports.statistics.generate(list(scalar)),
            )

            report = models.SqlalchemyProfiling(
                query=reports.sqlalchemy.generate(
                    sql=sql,  # type:ignore
                    orm=orm,  # type:ignore
                    explains=reports.postgres.generate(explains),
                ),
                allocation=reports.tracemalloc.generate(),
                garbage=reports.garbage.generate(),
            )

        return tables, report
