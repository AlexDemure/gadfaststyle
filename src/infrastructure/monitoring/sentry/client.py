import logging

import sentry_sdk

from sentry_sdk.integrations.logging import LoggingIntegration

from src.configuration import settings


class Sentry:
    @classmethod
    def start(cls) -> None:
        if not settings.SENTRY:
            return

        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            traces_sample_rate=1.0,
            environment=settings.SENTRY_ENV,
            debug=False,
            release="0.0.1",
            send_default_pii=True,
            integrations=[
                LoggingIntegration(
                    level=None,
                    event_level=logging.ERROR,
                )
            ],
        )

        logging.getLogger("sentry_sdk.errors").setLevel(logging.ERROR)

    def shutdown(self) -> None: ...
