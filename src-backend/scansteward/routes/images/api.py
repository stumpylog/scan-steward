from http import HTTPStatus
from mimetypes import guess_type

from django.db import transaction
from django.http import FileResponse
from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from django.shortcuts import get_object_or_404
from ninja import Router

from scansteward.common.constants import WEBP_CONTENT_TYPE
from scansteward.models import Image
from scansteward.models import Location
from scansteward.models import Person
from scansteward.models import PersonInImage
from scansteward.models import Pet
from scansteward.models import PetInImage
from scansteward.models import RoughDate
from scansteward.routes.images.schemas import ImageDetailsRead
from scansteward.routes.images.schemas import ImageUpdateSchema

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
)
def get_image_original(request: HttpRequest, image_id: int):
    img: Image = get_object_or_404(Image, id=image_id)

    mimetype, _ = guess_type(img.original_path)
    if not mimetype:
        mimetype = "image/jpeg"

    return FileResponse(img.original_path.open(mode="rb"), content_type=mimetype)


@router.get(
    "/{image_id}/details/",
    response={HTTPStatus.OK: ImageDetailsRead},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
def get_image_details(request: HttpRequest, image_id: int):
    return get_object_or_404(
        Image.objects.prefetch_related("people")
        .prefetch_related("albums")
        .prefetch_related("tags")
        .prefetch_related("pets")
        .prefetch_related("location")
        .prefetch_related("date"),
        id=image_id,
    )


@router.patch(
    "/{image_id}/details/",
    response={HTTPStatus.OK: ImageDetailsRead},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_image_details(request: HttpRequest, image_id: int, data: ImageUpdateSchema):
    instance: Image = await aget_object_or_404(Image, id=image_id)

    with transaction.atomic():

        if data.description:
            instance.description = data.description
        if data.orientation:
            instance.orientation = data.orientation

        if data.location_id:
            location: Location = await aget_object_or_404(Location, id=data.location_id)
            instance.location = location

        if data.date_id:
            date: RoughDate = await aget_object_or_404(RoughDate, id=data.date_id)
            instance.date = date

        if data.add_faces:
            for face_box in data.add_faces:
                person: Person = await aget_object_or_404(Person, id=face_box.person_id)
                _ = await PersonInImage.objects.acreate(
                    person=person,
                    image=instance,
                    center_x=face_box.box.center_x,
                    center_y=face_box.box.center_y,
                    height=face_box.box.height,
                    width=face_box.box.width,
                )
        if data.remove_faces:
            for face_box in data.remove_faces:
                person: Person = await aget_object_or_404(Person, id=face_box.person_id)
                await PersonInImage.objects.filter(
                    person=person,
                    image=instance,
                    center_x=face_box.box.center_x,
                    center_y=face_box.box.center_y,
                    height=face_box.box.height,
                    width=face_box.box.width,
                ).adelete()

        if data.add_pets:
            for pet_box in data.add_pets:
                pet: Pet = await aget_object_or_404(Pet, id=pet_box.pet_id)
                _ = await PetInImage.objects.acreate(
                    pet=pet,
                    image=instance,
                    center_x=pet_box.box.center_x,
                    center_y=pet_box.box.center_y,
                    height=pet_box.box.height,
                    width=pet_box.box.width,
                )
        if data.remove_pets:
            for pet_box in data.remove_pets:
                pet: Pet = await aget_object_or_404(Pet, id=pet_box.pet_id)
                await PetInImage.objects.filter(
                    pet=pet,
                    image=instance,
                    center_x=pet_box.box.center_x,
                    center_y=pet_box.box.center_y,
                    height=pet_box.box.height,
                    width=pet_box.box.width,
                ).adelete()

        instance.arefresh_from_db()
        return instance
