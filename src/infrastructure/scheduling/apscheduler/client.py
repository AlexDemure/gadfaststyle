import datetime
import typing

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.common.formats.utils import hashes
from src.configuration import settings

from .collections import ClientDisabled


class APScheduler:
    def __init__(self) -> None:
        self.scheduler: typing.Any | None = None

    def start(self) -> None:
        if not settings.SCHEDULER:
            return

        self.scheduler = AsyncIOScheduler(
            timezone=datetime.UTC,
            jobstores={"default": SQLAlchemyJobStore(settings.psycopg)},
            job_defaults={
                "coalesce": False,
                "max_instances": 1,
            },
        )

        self.scheduler.start()

    def shutdown(self) -> None:
        if not self.scheduler:
            return

        self.scheduler.shutdown()

    def add(
        self,
        func: typing.Callable[..., typing.Any],
        trigger: typing.Any,
        context: dict[str, typing.Any] | None = None,
    ) -> None:
        if not self.scheduler:
            raise ClientDisabled

        self.scheduler.add_job(
            func,
            trigger,
            id=hashes.deterministic(func, context),
            replace_existing=True,
            misfire_grace_time=3600,
            kwargs=context or {},
        )
