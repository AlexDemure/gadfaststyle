import jwt

from src.common.formats.utils import date
from src.common.formats.utils import uuid
from src.configuration import settings

from .collections import ClientDisabled
from .collections import TokenInvalid
from .collections import TokenPurpose
from .models import Token
from .models import Tokens


class JWT:
    @classmethod
    def encode(cls, subject: str) -> Tokens:
        if not settings.JWT:
            raise ClientDisabled

        jti = uuid.unique()

        access = Token(
            sub=subject,
            purpose=TokenPurpose.access,
            exp=int(date.shift(seconds=settings.JWT_ACCESS_EXPIRED_SECONDS).timestamp()),
            jti=jti,
        ).model_dump()

        refresh = Token(
            sub=subject,
            purpose=TokenPurpose.refresh,
            exp=int(date.shift(seconds=settings.JWT_REFRESH_EXPIRED_SECONDS).timestamp()),
            jti=jti,
        ).model_dump()

        return Tokens(
            access=jwt.encode(payload=access, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM),
            refresh=jwt.encode(payload=refresh, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM),
        )

    @classmethod
    def decode(cls, token: str, purpose: TokenPurpose) -> Token:
        if not settings.JWT:
            raise ClientDisabled

        try:
            signature = Token(**jwt.decode(token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]))
            if signature.purpose is not purpose:
                raise jwt.PyJWTError
        except jwt.PyJWTError:
            raise TokenInvalid
        return signature
