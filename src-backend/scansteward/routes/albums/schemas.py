import sys

from ninja import Field
from ninja import Schema
from pydantic import model_validator

if sys.version_info > (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class AlbumCreateSchema(Schema):
    name: str = Field(description="The name of the album")
    description: str | None = Field(default=None, description="The description of the album")


class AlbumBasicReadSchema(AlbumCreateSchema):
    id: int = Field(description="The id of the album")


class AlbumWithImagesReadSchema(AlbumBasicReadSchema):
    image_ids: list[int] = Field(description="The ids of the images in this album in sorted order")


class AlbumUpdateSchema(Schema):
    name: str | None = Field(default=None, description="The new name of the album")
    description: str | None = Field(default=None, description="The new description of the album")

    @model_validator(mode="after")
    def check_one_or_other(self) -> Self:
        if self.name is None and self.description is None:
            raise ValueError("At least one of name or description must be set")  # noqa: TRY003, EM101
        return self


class AlbumSortUpdate(Schema):
    sorting: list[int] = Field(
        description="The new order of the images, with the index being the new position in the album",
    )


class AlbumAddImageSchema(Schema):
    image_id: int = Field(default=None, description="The id of the image to add to the album")


class AlbumRemoveImageSchema(Schema):
    image_id: int = Field(default=None, description="The id of the image to remove from the album")
