from http import HTTPStatus
from mimetypes import guess_type
from typing import TYPE_CHECKING

from django.http import FileResponse
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from ninja import Router
from ninja.decorators import decorate_view

from scansteward.common.constants import WEBP_CONTENT_TYPE
from scansteward.models import Image
from scansteward.models import PersonInImage
from scansteward.models import PetInImage
from scansteward.routes.images.conditionals import full_size_etag
from scansteward.routes.images.conditionals import image_last_modified
from scansteward.routes.images.conditionals import original_image_etag
from scansteward.routes.images.conditionals import thumbnail_etag
from scansteward.routes.images.schemas import BoundingBox
from scansteward.routes.images.schemas import ImageMetadataRead
from scansteward.routes.images.schemas import PersonWithBox
from scansteward.routes.images.schemas import PetWithBox

router = Router(tags=["images"])


@router.get(
    "/{image_id}/thumbnail/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.OK: {
                "content": {WEBP_CONTENT_TYPE: {"schema": {"type": "string", "format": "binary"}}},
            },
        },
    },
    operation_id="get_image_thumbnail",
)
@decorate_view(
    cache_control(private=True, max_age=3600),
    condition(last_modified_func=image_last_modified, etag_func=thumbnail_etag),
)
def get_image_thumbnail(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    return FileResponse(img.thumbnail_path.open(mode="rb"), content_type=WEBP_CONTENT_TYPE)


@router.get(
    "/{image_id}/full/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.OK: {
                "content": {WEBP_CONTENT_TYPE: {"schema": {"type": "string", "format": "binary"}}},
            },
        },
    },
    operation_id="get_image_full_size",
)
@decorate_view(
    cache_control(private=True, max_age=3600),
    condition(last_modified_func=image_last_modified, etag_func=full_size_etag),
)
def get_image_full_size(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    return FileResponse(img.full_size_path.open(mode="rb"), content_type=WEBP_CONTENT_TYPE)


@router.get(
    "/{image_id}/original/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.OK: {"content": {"image/*": {"schema": {"type": "string", "format": "binary"}}}},
        },
    },
    operation_id="get_image_original",
)
@decorate_view(
    cache_control(private=True, max_age=3600),
    condition(last_modified_func=image_last_modified, etag_func=original_image_etag),
)
def get_image_original(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    mimetype, _ = guess_type(img.original_path)
    if not mimetype:
        mimetype = "image/jpeg"

    return FileResponse(img.original_path.open(mode="rb"), content_type=mimetype)


@router.get(
    "/{image_id}/faces/",
    response={HTTPStatus.OK: list[PersonWithBox]},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="get_faces_in_images",
)
async def get_faces_in_images(request: HttpRequest, image_id: int):
    # TODO: I bet there's some clever SQL to grab this more efficiently

    img: Image = await aget_object_or_404(Image.objects.prefetch_related("people"), id=image_id)

    all_people_in_image = img.people.prefetch_related("images").all()

    boxes: list[PersonWithBox] = []
    async for person in all_people_in_image:
        bounding_box: PersonInImage = await person.images.aget(image=img)

        if TYPE_CHECKING:
            assert bounding_box is not None
            assert isinstance(bounding_box, PersonInImage)

        boxes.append(
            PersonWithBox(
                person_id=person.pk,
                box=BoundingBox(
                    center_x=bounding_box.center_x,
                    center_y=bounding_box.center_y,
                    height=bounding_box.height,
                    width=bounding_box.width,
                ),
            ),
        )

    return boxes


@router.get(
    "/{image_id}/pets/",
    response={HTTPStatus.OK: list[PetWithBox]},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="get_pets_in_images",
)
async def get_pets_in_images(request: HttpRequest, image_id: int):
    # TODO: I bet there's some clever SQL to grab this more efficiently

    img: Image = await aget_object_or_404(Image.objects.prefetch_related("pets"), id=image_id)

    all_pets_in_image = img.pets.prefetch_related("images").all()

    boxes: list[PetWithBox] = []
    async for pet in all_pets_in_image:
        bounding_box: PetInImage = await pet.images.aget(image=img)

        if TYPE_CHECKING:
            assert bounding_box is not None
            assert isinstance(bounding_box, PetInImage)

        boxes.append(
            PersonWithBox(
                person_id=pet.pk,
                box=BoundingBox(
                    center_x=bounding_box.center_x,
                    center_y=bounding_box.center_y,
                    height=bounding_box.height,
                    width=bounding_box.width,
                ),
            ),
        )

    return boxes


@router.get(
    "/{image_id}/metadata/",
    response={HTTPStatus.OK: ImageMetadataRead},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="get_image_metadata",
)
async def get_image_metadata(request: HttpRequest, image_id: int):
    # TODO: I bet there's some clever SQL to grab this more efficiently

    img: Image = await aget_object_or_404(
        Image.objects.prefetch_related("albums")
        .prefetch_related("tags")
        .prefetch_related("location")
        .prefetch_related("date"),
        id=image_id,
    )

    tags = [pk async for pk in img.tags.all().only("pk").values_list("pk", flat=True)]
    albums = [pk async for pk in img.albums.all().only("pk").values_list("pk", flat=True)]

    return ImageMetadataRead(
        orientation=img.orientation,
        description=img.description,
        location_id=img.location.pk if img.location else None,
        date_id=img.date.pk if img.date else None,
        tag_ids=tags if tags else None,
        album_ids=albums if albums else None,
    )
