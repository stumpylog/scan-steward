from datetime import date

from ninja import Schema
from simpleiso3166.countries.types import CountryCodeAlpha2Type
from simpleiso3166.subdivisions.types import SubdivisionCodeType

from scansteward.common.schemas import SimpleNamedWithIdSchema
from scansteward.imageops.models import RotationEnum
from scansteward.routes.tags.schemas import TagRead


class Album(SimpleNamedWithIdSchema):
    pass


class BoundingBox(Schema):
    center_x: float
    center_y: float
    height: float
    width: float


class PersonWithBox(Schema):
    person_id: int
    box: BoundingBox


class PetWithBox(Schema):
    pet_id: int
    box: BoundingBox


class ImageLocation(Schema):
    country_code: CountryCodeAlpha2Type
    subdivision_code: SubdivisionCodeType | None = None
    city: str | None = None
    sub_location: str | None = None


class ImageDate(Schema):
    date: date
    month_valid: bool
    day_valid: bool


class ImageDetailsRead(Schema):
    orientation: RotationEnum
    face_boxes: list[PersonWithBox] | None = None
    pet_boxes: list[PetWithBox] | None = None
    tags: list[TagRead] | None = None
    albums: list[Album] | None = None
    description: str | None = None
    location: ImageLocation | None = None
    date: ImageDate | None = None


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
