from __future__ import annotations

import sys

from ninja import Field
from ninja import Schema
from pydantic import model_validator
from pydantic_extra_types.country import CountryAlpha2  # noqa: TCH002 (required for schema to build)

if sys.version_info > (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class LocationCreateSchema(Schema):
    """
    Schema to create a Location
    """

    country_code: CountryAlpha2 = Field(description="The ISO 3166-1 alpha-2 code of the country")
    subdivision_code: str | None = Field(
        default=None,
        description="The ISO 3166-2 subdivision code of the location",
    )
    city: str | None = Field(default=None, description="The city of the location")
    sub_location: str | None = Field(default=None, description="The location taken or shown")


class LocationReadSchema(LocationCreateSchema):
    """
    Schema to create a Location
    """

    id: int = Field(description="The id of the location")


class LocationUpdateSchema(Schema):
    """
    Schema to create a Location
    """

    country_code: CountryAlpha2 | None = Field(
        default=None,
        description="The new ISO 3166-1 alpha-2 code of the country",
    )
    subdivision_code: str | None = Field(
        default=None,
        description="The new ISO 3166-2 subdivision code of the location",
    )
    city: str | None = Field(default=None, description="The new city of the location")
    sub_location: str | None = Field(default=None, description="The new location taken or shown")

    @model_validator(mode="after")
    def check_country_with_subdivision(self) -> Self:
        if self.subdivision_code and not self.country_code:
            msg = "Subdivision must also include country code"
            raise ValueError(msg)
        return self
