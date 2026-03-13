from src.infrastructure.databases.postgres.tables import Account as _Account

from .base import Table


class Account(Table):
    class Meta:
        model = _Account
