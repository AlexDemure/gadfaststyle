from src.entrypoints.http.common.collections.exceptions import Forbidden
from src.infrastructure.security.jwt.collections import TokenInvalid


AUTHORIZATION_ERRORS = [
    Forbidden,
    TokenInvalid,
]
