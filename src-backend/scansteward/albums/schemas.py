from ninja import Schema


class AlbumCreateSchema(Schema):
    name: str
    description: str | None = None


class AlbumBasicReadSchema(AlbumCreateSchema):
    id: int


class AlbumWithImagesReadSchema(AlbumBasicReadSchema):
    image_ids: list[int]


class AlbumUpdateSchema(Schema):
    name: str | None = None
    description: str | None = None


class ImageSortSettingSchema(Schema):
    image_id: int
    sort_order: int


class AlbumSortUpdate(Schema):
    sorting: list[ImageSortSettingSchema]


class AlbumAddImageSchema(Schema):
    image_id: int
