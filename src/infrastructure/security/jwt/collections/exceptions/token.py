from src.common.http.collections import HTTPCode
from src.common.http.collections import HTTPError


class TokenInvalid(HTTPError):
    code = HTTPCode.UNAUTHORIZED
