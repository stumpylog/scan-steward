from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from ninja import Schema
from pydantic import model_validator

if TYPE_CHECKING:
    from pydantic_extra_types.country import CountryAlpha2

if sys.version_info > (3, 11):
    from typing import Self

else:
    from typing_extensions import Self


class LocationCreateSchema(Schema):
    """
    Schema to create a Person
    """

    country_code: CountryAlpha2
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

    country_code: CountryAlpha2 | None = None
    subdivision_code: str | None = None
    city: str | None = None
    sub_location: str | None = None

    @model_validator(mode="after")
    def check_country_with_subdivision(self) -> Self:
        if self.subdivision_code and not self.country_code:
            msg = "Subdivision must also include country code"
            raise ValueError(msg)
        return self
