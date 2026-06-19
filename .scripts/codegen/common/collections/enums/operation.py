import enum


class Operation(enum.StrEnum):
    ONE = "one"
    LIST = "list"
    PAGINATED = "paginated"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    EXISTS = "exists"
