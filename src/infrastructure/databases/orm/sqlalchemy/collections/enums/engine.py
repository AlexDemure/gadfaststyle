import enum


class Isolation(enum.StrEnum):
    autocommit = "AUTOCOMMIT"
    read_committed = "READ COMMITTED"
    read_uncommitted = "READ UNCOMMITTED"
    repeatable_read = "REPEATABLE READ"
    serializable = "SERIALIZABLE"
