from src.common.http.collections import HTTPCode
from src.common.http.collections import HTTPError


class BusinessError(HTTPError):
    code = HTTPCode.IM_A_TEAPOT
