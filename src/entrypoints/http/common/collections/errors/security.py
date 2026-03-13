from src.common.http.collections import Forbidden
from src.infrastructure.security.jwt.collections import TokenInvalid


AUTHORIZATION_ERRORS = [
    Forbidden,
    TokenInvalid,
]
