import logging
from http import HTTPStatus

from django.db import transaction
from django.db.models import Max
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.albums.schemas import AlbumAddImageSchema
from scansteward.albums.schemas import AlbumBasicReadSchema
from scansteward.albums.schemas import AlbumCreateSchema
from scansteward.albums.schemas import AlbumSortUpdate
from scansteward.albums.schemas import AlbumUpdateSchema
from scansteward.albums.schemas import AlbumWithImagesReadSchema
from scansteward.models import Album
from scansteward.models import Image
from scansteward.models import ImageInAlbum

router = Router(tags=["albums"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[AlbumBasicReadSchema])
@paginate(LimitOffsetPagination)
def get_albums(request: HttpRequest):
    return Album.objects.all()


@router.get(
    "/{album_id}",
    response=AlbumWithImagesReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def get_album(request: HttpRequest, album_id: int):
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)

    return album_instance


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


@router.patch(
    "/{album_id}/add",
    response=AlbumWithImagesReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def add_image_to_album(request: HttpRequest, album_id: int, data: AlbumAddImageSchema):
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)
    image_instance: Image = get_object_or_404(Image, id=data.image_id)

    sort_order = (
        ImageInAlbum.objects.filter(album=album_instance).aggregate(Max("sort_order", default=0))[
            "sort_order__max"
        ]
        + 1
    )
    logger.info(sort_order)

    _ = ImageInAlbum.objects.get_or_create(
        album=album_instance,
        image=image_instance,
        sort_order=sort_order,
    )
    album_instance.refresh_from_db()

    return album_instance


@router.patch(
    "/{album_id}/sort",
    response=AlbumWithImagesReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def update_album_sorting(request: HttpRequest, album_id: int, data: AlbumSortUpdate):
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)

    with transaction.atomic():

        # For a moment, reset the sorting order to be above the current largest
        temp_sort_order = (
            ImageInAlbum.objects.filter(album=album_instance).aggregate(Max("sort_order", default=0))[
                "sort_order__max"
            ]
            + 1
        )
        for image_in_album_instance in ImageInAlbum.objects.filter(album=album_instance).all():
            image_in_album_instance.sort_order = temp_sort_order
            image_in_album_instance.save()
            temp_sort_order += 1

        for sort_setting in data.sorting:
            image_instance = get_object_or_404(Image, id=sort_setting.image_id)
            image_in_album_instance = get_object_or_404(
                ImageInAlbum,
                album=album_instance,
                image=image_instance,
            )
            image_in_album_instance.sort_order = sort_setting.sort_order
            image_in_album_instance.save()

    album_instance.refresh_from_db()

    return album_instance
