from http import HTTPStatus

from django.http import FileResponse
from django.http import Http404
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from scansteward.images.schemas import ImageDetailsRead
from scansteward.models import Image

router = Router(tags=["images"])


@router.get(
    "/{image_id}/thumbnail/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def get_image_thumbnail(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    return FileResponse(img.thumbnail_path.open(mode="rb"), content_type="image/webp")


@router.get(
    "/{image_id}/full/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def get_image_full_size(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    return FileResponse(img.full_size_path.open(mode="rb"), content_type="image/webp")


@router.get(
    "/{image_id}/original/",
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_image_original(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    return FileResponse(img.original_path.open(mode="rb"), content_type="image/webp")


@router.patch(
    "/{image_id}/",
    response={HTTPStatus.OK: ImageDetailsRead},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_image_details(request: HttpRequest, image_id: int):
    try:
        return (
            await Image.objects.prefetch_related("people")
            .prefetch_related("albums")
            .prefetch_related("tags")
            .aget(id=image_id)
        )
    except Image.DoesNotExist:
        raise Http404 from None
