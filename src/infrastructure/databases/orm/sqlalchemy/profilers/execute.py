import logging
import time
import typing

from sqlalchemy import Executable
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger("postgres.profiler")


def profiler(session: AsyncSession) -> None:
    execute = session.execute

    async def _execute(statement: Executable, *args: typing.Any, **kwargs: typing.Any) -> Result[typing.Any] | None:
        start = time.perf_counter()
        try:
            return await execute(statement, *args, **kwargs)
        finally:
            if hasattr(statement, "compile"):
                compiled = statement.compile(dialect=session.bind.dialect, compile_kwargs={"literal_binds": True})
                logger.info(str(compiled), extra={"elapsed": time.perf_counter() - start})

    setattr(session, "execute", _execute)
