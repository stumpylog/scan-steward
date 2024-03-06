from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.albums.schemas import AlbumBasicReadSchema
from scansteward.albums.schemas import AlbumCreateSchema
from scansteward.albums.schemas import AlbumUpdateSchema
from scansteward.models import Album

router = Router(tags=["albums"])


@router.get("/", response=list[AlbumBasicReadSchema])
@paginate(LimitOffsetPagination)
def get_albums(request: HttpRequest):
    return Album.objects.all()


@router.get(
    "/{album_id}",
    response=list[AlbumBasicReadSchema],
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_album(request: HttpRequest, album_id: int):
    # TODO: This needs to return the list of image IDs along with the name and description
    pass


@router.post("/", response={HTTPStatus.CREATED: AlbumBasicReadSchema})
async def create_album(request: HttpRequest, data: AlbumCreateSchema):
    instance: Album = await Album.objects.acreate(
        name=data.name,
        description=data.description,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{album_id}",
    response=AlbumBasicReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_album(request: HttpRequest, album_id: int, data: AlbumUpdateSchema):
    instance: Album = await aget_object_or_404(Album, id=album_id)
    if data.name is not None:
        instance.name = data.name
    if data.description is not None:
        instance.description = data.description
    await instance.asave()
    await instance.arefresh_from_db()
    return instance
