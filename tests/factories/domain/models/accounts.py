import typing

from factory import Factory
from factory import LazyFunction

from src.common.formats.utils import date
from src.domain.models import Account as _Account

from tests.faker import fake


class Account(Factory[_Account]):
    class Meta:
        model = _Account

    id = None
    external_id = LazyFunction(fake.uuid4)
    created = LazyFunction(fake.date_time)
    updated = LazyFunction(fake.date_time)
    blocked = None
    authorization = LazyFunction(fake.date_time)

    @classmethod
    def init(cls, external_id: str) -> typing.Self:
        created = updated = date.now()

        return cls(
            id=None,
            external_id=external_id,
            created=created,
            updated=updated,
            blocked=None,
            authorization=None,
        )
