import datetime
import typing

from datetime import date

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import model_validator


class DateRange(BaseModel):
    started: datetime.date
    ended: datetime.date | None = None

    @field_validator("started")
    @classmethod
    def validate_started_not_future(cls, value: datetime.date) -> datetime.date:
        if value > date.today():
            raise ValueError("started date cannot be in the future")
        return value

    @field_validator("ended")
    @classmethod
    def validate_ended_not_future(cls, value: datetime.date | None) -> datetime.date | None:
        if value and value > date.today():
            raise ValueError("ended date cannot be in the future")
        return value

    @model_validator(mode="after")
    def validate_date_order(self) -> typing.Self:
        if self.ended and self.started > self.ended:
            raise ValueError("started date must be before ended date")
        return self
