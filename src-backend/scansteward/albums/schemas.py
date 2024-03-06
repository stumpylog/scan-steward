from ninja import Schema


class AlbumCreateSchema(Schema):
    name: str
    description: str | None = None


class AlbumBasicReadSchema(AlbumCreateSchema):
    id: int


class AlbumWithImagesReadSchema(AlbumBasicReadSchema):
    images: list[int]


class AlbumUpdateSchema(Schema):
    id: int
    name: str | None = None
    description: str | None = None


class AlbumSortUpdate(Schema):
    id: int
    sorting: dict[int, int]
