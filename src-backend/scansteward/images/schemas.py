from ninja import Schema

from scansteward.common.schemas import SimpleNamedWithIdSchema
from scansteward.people.schemas import PersonRead
from scansteward.tags.schemas import TagRead


class Album(SimpleNamedWithIdSchema):
    pass


class ImageDetailsRead(Schema):
    people: list[PersonRead] | None = None
    tags: list[TagRead] | None = None
    albums: list[Album] | None = None
