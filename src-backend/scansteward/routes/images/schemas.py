from datetime import date as std_date

from ninja import Field
from ninja import Schema
from simpleiso3166.countries.types import CountryCodeAlpha2Type
from simpleiso3166.subdivisions.types import SubdivisionCodeType

from scansteward.imageops.models import RotationEnum


class Album(Schema):
    id: int
    name: str
    description: str | None = None


class BoundingBox(Schema):
    center_x: float = Field(description="Center X coordinate of the bounding box")
    center_y: float = Field(description="Center Y coordinate of the bounding box")
    height: float = Field(description="Height of the bounding box")
    width: float = Field(description="Width of the bounding box")


class PersonWithBox(Schema):
    person_id: int = Field(description="Person ID")
    box: BoundingBox = Field(description="Bounding box of the person's face")


class PetWithBox(Schema):
    pet_id: int = Field(description="Pet ID")
    box: BoundingBox = Field(description="Bounding box of the pet")


class ImageLocation(Schema):
    country_code: CountryCodeAlpha2Type = Field(description="Country code where the image was taken")
    subdivision_code: SubdivisionCodeType | None = Field(
        default=None,
        description="Subdivision code where the image was taken",
    )
    city: str | None = Field(default=None, description="City where the image was taken")
    sub_location: str | None = Field(default=None, description="Sub location where the image was taken")


class ImageDate(Schema):
    date: std_date = Field(description="Date of the image")
    month_valid: bool = Field(description="Whether the month is valid")
    day_valid: bool = Field(description="Whether the day is valid")


class ImageMetadataRead(Schema):
    orientation: RotationEnum
    description: str | None = None
    location_id: int | None = None
    date_id: int | None = None
    tag_ids: list[int] | None = None
    album_ids: list[int] | None = None


class ImageUpdateSchema(Schema):
    add_faces: list[PersonWithBox] | None = None
    remove_faces: list[PersonWithBox] | None = None

    add_pets: list[PetWithBox] | None = None
    remove_pets: list[PetWithBox] | None = None

    location_id: int | None = None
    date_id: int | None = None

    description: str | None = None

    orientation: RotationEnum | None = None

    # TODO: Tags????
