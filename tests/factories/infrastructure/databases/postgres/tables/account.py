import factory

from src.common.formats.utils import date
from src.infrastructure.databases.postgres import tables

from tests.faker import fake

from .base import Table


class Account(Table):
    class Meta:
        model = tables.Account

    external_id = factory.LazyFunction(fake.uuid4)
    created = factory.LazyFunction(date.now)
    updated = factory.LazyAttribute(lambda object_: object_.created)
