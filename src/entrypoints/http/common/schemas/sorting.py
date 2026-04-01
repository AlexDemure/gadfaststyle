import uuid

from pydantic import BaseModel


class Sorted(BaseModel):
    seed: uuid.UUID
