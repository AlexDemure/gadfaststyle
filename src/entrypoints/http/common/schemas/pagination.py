import typing

from pydantic import BaseModel
from pydantic import Field


class Pagination(BaseModel):
    page: typing.Annotated[int, Field(gt=0, le=1000)]
    size: typing.Annotated[int, Field(gt=0, le=100)]

    @property
    def convert(self) -> dict[str, int]:
        return dict(limit=self.size, offset=(self.page - 1) * self.size if self.page > 0 else 0)


class Paginated(BaseModel):
    total: int
    items: list[typing.Any]
