import datetime
import sys

from ninja import Schema
from pydantic import model_validator

if sys.version_info > (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class RoughDateCreateSchema(Schema):
    """
    Schema to create a Person
    """

    date: datetime.date
    month_valid: bool = False
    day_valid: bool = False

    @model_validator(mode="after")
    def check_one_or_other(self) -> Self:
        if self.day_valid and not self.month_valid:
            raise ValueError("A day cannot be valid if the month is not valid")  # noqa: TRY003, EM101
        return self


class RoughDateReadSchema(RoughDateCreateSchema):
    """
    Schema when reading a person
    """

    id: int


class RoughDateUpdateSchema(Schema):
    """
    Schema to update a person
    """

    date: datetime.date | None = None
    month_valid: bool | None = None
    day_valid: bool | None = None

    @model_validator(mode="after")
    def check_one_or_other(self) -> Self:
        if self.date is None and self.month_valid is None and self.day_valid is None:
            raise ValueError("At least one of name or description must be set")  # noqa: TRY003, EM101
        return self
