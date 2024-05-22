from ninja import Field
from ninja import Schema

from scansteward.imageops.models import RotationEnum


class Album(Schema):
    id: int
    name: str
    description: str | None = None


class BoundingBoxSchema(Schema):
    center_x: float = Field(description="Center X coordinate of the bounding box")
    center_y: float = Field(description="Center Y coordinate of the bounding box")
    height: float = Field(description="Height of the bounding box")
    width: float = Field(description="Width of the bounding box")


class PersonWithBoxSchema(Schema):
    person_id: int = Field(description="Person ID")
    box: BoundingBoxSchema = Field(description="Bounding box of the person's face")


class PetWithBoxSchema(Schema):
    pet_id: int = Field(description="Pet ID")
    box: BoundingBoxSchema = Field(description="Bounding box of the pet")


class ImageMetadataReadSchema(Schema):
    orientation: RotationEnum
    description: str | None = None
    location_id: int | None = None
    date_id: int | None = None
    tag_ids: list[int] | None = None
    album_ids: list[int] | None = None


class ImageMetadataUpdateSchema(Schema):
    description: str | None = None

    orientation: RotationEnum | None = None

    location_id: int | None = None
    date_id: int | None = None
