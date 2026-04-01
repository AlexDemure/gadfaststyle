import typing

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer


def dependency(
    authorization: typing.Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(bearerFormat="JWT"))],
) -> str:
    return authorization.credentials
