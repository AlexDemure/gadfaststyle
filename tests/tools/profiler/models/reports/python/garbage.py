from pydantic import BaseModel


class GarbageCollector(BaseModel):
    collected: int
    uncollectable: int
