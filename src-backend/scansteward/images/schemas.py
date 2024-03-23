from ninja import Schema
from pydantic_extra_types.country import CountryAlpha2

from scansteward.common.schemas import SimpleNamedWithIdSchema
from scansteward.imageops.models import RotationEnum
from scansteward.people.schemas import PersonReadSchema
from scansteward.pets.schemas import PetReadSchema
from scansteward.tags.schemas import TagRead


class Album(SimpleNamedWithIdSchema):
    pass


class BoundingBox(Schema):
    center_x: float
    center_y: float
    height: float
    width: float


class ThingWithBox(Schema):
    box: BoundingBox


class PersonWithBox(ThingWithBox):
    person: PersonReadSchema


class PetWithBox(ThingWithBox):
    pet: PetReadSchema


class ImageLocation(Schema):
    country_code: CountryAlpha2
    subdivision_code: str | None = None
    city: str | None = None
    sub_location: str | None = None


class ImageDetailsRead(Schema):
    orientation: RotationEnum
    face_boxes: list[PersonWithBox] | None = None
    pet_boxes: list[PetWithBox] | None = None
    tags: list[TagRead] | None = None
    albums: list[Album] | None = None
    description: str | None = None
    location: ImageLocation | None = None


class ImageUpdateSchema(Schema):
    add_faces: list[PersonWithBox] | None = None
    remove_faces: list[PersonWithBox] | None = None

    add_pets: list[PetWithBox] | None = None
    remove_pets: list[PetWithBox] | None = None

    country: str | None = None
    state: str | None = None
    city: str | None = None

    description: str | None = None

    orientation: RotationEnum | None = None

    # TODO: Tags????
