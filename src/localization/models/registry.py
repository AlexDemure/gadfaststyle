from pydantic import BaseModel


class Localization(BaseModel):
    errors: dict[str, str] = {}
    http: dict[int, str] = {}
