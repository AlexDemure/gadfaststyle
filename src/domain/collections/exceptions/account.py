from src.common.http.collections import HTTPCode
from src.common.http.collections import HTTPError


class AccountAlreadyExists(HTTPError):
    code = HTTPCode.CONFLICT


class AccountBlocked(HTTPError):
    code = HTTPCode.FORBIDDEN


class AccountNotFound(HTTPError):
    code = HTTPCode.NOT_FOUND
