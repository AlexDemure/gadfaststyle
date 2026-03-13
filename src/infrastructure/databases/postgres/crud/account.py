from src.infrastructure.databases.orm.sqlalchemy.crud import Base
from src.infrastructure.databases.postgres import tables


class Account(Base[tables.Account]):
    table = tables.Account
