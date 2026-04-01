from pydantic import BaseModel


class Statistics(BaseModel):
    mean: float
    median: float
    stdev: float
    min: float
    max: float
