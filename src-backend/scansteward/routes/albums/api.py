import logging
import tempfile
import zipfile
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

from django.db import transaction
from django.db.models import Max
from django.http import FileResponse
from django.http import Http404
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http400Error
from scansteward.models import Album
from scansteward.models import Image
from scansteward.models import ImageInAlbum
from scansteward.routes.albums.schemas import AlbumAddImageSchema
from scansteward.routes.albums.schemas import AlbumBasicReadSchema
from scansteward.routes.albums.schemas import AlbumCreateSchema
from scansteward.routes.albums.schemas import AlbumRemoveImageSchema
from scansteward.routes.albums.schemas import AlbumSortUpdate
from scansteward.routes.albums.schemas import AlbumUpdateSchema
from scansteward.routes.albums.schemas import AlbumWithImagesReadSchema

router = Router(tags=["albums"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[AlbumBasicReadSchema])
@paginate(LimitOffsetPagination)
def get_albums(request: HttpRequest):
    return Album.objects.all()


@router.get(
    "/{album_id}/",
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
    "/{album_id}/",
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
    instance.description = data.description
    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.patch(
    "/{album_id}/add/",
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

    _ = ImageInAlbum.objects.get_or_create(
        album=album_instance,
        image=image_instance,
        sort_order=sort_order,
    )
    album_instance.refresh_from_db()

    return album_instance


@router.patch(
    "/{album_id}/remove/",
    response=AlbumWithImagesReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def remove_image_from_album(request: HttpRequest, album_id: int, data: AlbumRemoveImageSchema):
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)
    image_instance: Image = get_object_or_404(Image, id=data.image_id)

    if not album_instance.images.filter(pk=data.image_id).exists():
        msg = f"Image {data.image_id} not in album"
        logger.error(msg)
        raise Http404(msg)

    album_instance.images.remove(image_instance)

    album_instance.refresh_from_db()

    return album_instance


@router.patch(
    "/{album_id}/sort/",
    response=AlbumWithImagesReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.BAD_REQUEST: {
                "description": "Sorting data did not match album image count",
            },
        },
    },
)
def update_album_sorting(request: HttpRequest, album_id: int, data: AlbumSortUpdate):
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)

    if album_instance.images.count() != len(data.sorting):
        msg = f"Album contains {album_instance.images.count()} images, but {len(data.sorting)} sorting values were provided."
        logger.error(msg)
        raise Http400Error(msg)

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

        for index, image_id in enumerate(data.sorting):
            image_instance = get_object_or_404(Image, id=image_id)
            image_in_album_instance = get_object_or_404(
                ImageInAlbum,
                album=album_instance,
                image=image_instance,
            )
            image_in_album_instance.sort_order = index
            image_in_album_instance.save()

    album_instance.refresh_from_db()

    return album_instance


@router.delete(
    "/{album_id}/",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def delete_album(request: HttpRequest, album_id: int):
    instance: Album = await aget_object_or_404(Album, id=album_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None


@router.get(
    "/{album_id}/download/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.BAD_REQUEST: {
                "description": "No images in album",
            },
            HTTPStatus.OK: {
                "content": {"application/zip": {"schema": {"type": "string", "format": "binary"}}},
            },
        },
    },
)
def download_album(request: HttpRequest, album_id: int, zip_originals: bool = False):  # noqa: FBT001, FBT002
    album_instance: Album = get_object_or_404(Album.objects.prefetch_related("images"), id=album_id)

    if album_instance.images.count() == 0:
        msg = f"Album {album_instance.name} has no images"
        logger.error(msg)
        raise Http400Error(msg)

    zip_name = slugify(album_instance.name)
    # TODO: Track and clean these up on a schedule
    zip_path = Path(tempfile.NamedTemporaryFile(prefix=f"{zip_name}", suffix=".zip", delete=False).name)
    with zipfile.ZipFile(zip_path, mode="w") as output_zip:
        for index, image in enumerate(album_instance.images.order_by("imageinalbum__sort_order").all()):
            if TYPE_CHECKING:
                assert isinstance(image, Image)
            if zip_originals:
                output_zip.write(image.original_path, arcname=f"{index + 1:010}{image.original_path.suffix}")
            else:
                output_zip.write(
                    image.full_size_path,
                    arcname=f"{index + 1:010}{image.full_size_path.suffix}",
                )

    return FileResponse(zip_path.open(mode="rb"), content_type="application/zip", as_attachment=True)
