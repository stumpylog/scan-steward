from ninja import Schema

from scansteward.common.schemas import SimpleNamedWithIdSchema
from scansteward.people.schemas import PersonRead
from scansteward.tags.schemas import TagRead


class Album(SimpleNamedWithIdSchema):
    pass


class BoundingBox(Schema):
    center_x: float
    center_y: float
    height: float
    width: float


class PersonWithBox(Schema):
    person: PersonRead
    box: BoundingBox


class ImageDetailsRead(Schema):
    face_boxes: list[PersonWithBox] | None = None
    tags: list[TagRead] | None = None
    albums: list[Album] | None = None
