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


class AlbumSortUpdate(Schema):
    sorting: list[int]


class AlbumAddImageSchema(Schema):
    image_id: int


class AlbumRemoveImageSchema(AlbumAddImageSchema):
    pass
