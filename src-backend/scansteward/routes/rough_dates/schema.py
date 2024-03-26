import datetime

from ninja import Schema


class RoughDateCreateSchema(Schema):
    """
    Schema to create a Person
    """

    date: datetime.date
    month_valid: bool = False
    day_valid: bool = False


class RoughDateReadSchema(RoughDateCreateSchema):
    """
    Schema when reading a person
    """

    id: int


class RoughDateUpdateSchema(Schema):
    """
    Schema to update a person
    """

    # TODO: Validate one or both fields provided
    date: datetime.date | None = None
    month_valid: bool | None = None
    day_valid: bool | None = None
