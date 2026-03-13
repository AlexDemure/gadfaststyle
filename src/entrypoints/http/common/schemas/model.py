import typing

from src.domain.models import Model

from .http import Response


class ID(Response):
    id: int | str

    @classmethod
    def serialize(cls, model: Model) -> typing.Self:
        if not hasattr(model, "id"):
            raise ValueError
        return cls(id=model.id)
