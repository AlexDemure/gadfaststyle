from .base import BusinessError


class AccountAlreadyExists(BusinessError): ...


class AccountBlocked(BusinessError): ...


class AccountNotFound(BusinessError): ...
