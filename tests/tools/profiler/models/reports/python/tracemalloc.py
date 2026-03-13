from pydantic import BaseModel


class Allocation(BaseModel):
    current: float
    peak: float
