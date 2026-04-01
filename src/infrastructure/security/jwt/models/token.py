from pydantic import BaseModel

from src.infrastructure.security.jwt.collections import TokenPurpose


class Token(BaseModel):
    sub: str
    purpose: TokenPurpose
    exp: int
    jti: str


class Tokens(BaseModel):
    access: str
    refresh: str
