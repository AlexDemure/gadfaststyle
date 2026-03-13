from src.domain import models
from src.domain.collections import exceptions
from src.infrastructure.databases.postgres import crud
from src.infrastructure.databases.postgres import tables

from .base import Base


class Account(Base[crud.Account, tables.Account, models.Account, exceptions.AccountNotFound]):
    crud = crud.Account
    table = tables.Account
    model = models.Account
    error = exceptions.AccountNotFound
