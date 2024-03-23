from ninja import Schema
from pydantic_extra_types.country import CountryAlpha2


class LocationCreateSchema(Schema):
    """
    Schema to create a Person
    """

    country_alpha_2_code: CountryAlpha2
    subdivision_code: str | None = None
    city: str | None = None
    sub_location: str | None = None

    # TODO: Validate the state is valid for the country


class LocationReadSchema(LocationCreateSchema):
    """
    Schema to create a Person
    """

    id: int


class LocationUpdateSchema(Schema):
    """
    Schema to create a Person
    """

    country_alpha_2_code: CountryAlpha2 | None = None
    subdivision_code: str | None = None
    city: str | None = None
    sub_location: str | None = None
