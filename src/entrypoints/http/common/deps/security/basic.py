import typing

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from src.configuration import settings


def dependency(authenticate: typing.Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]) -> None:
    if settings.AUTHENTICATION:
        if not (
            (authenticate.username == settings.AUTHENTICATION_HTTP_BASIC_USERNAME)
            and (authenticate.password == settings.AUTHENTICATION_HTTP_BASIC_PASSWORD)
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Basic"})
