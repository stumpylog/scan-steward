from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.models import Pet
from scansteward.pets.schemas import PetCreateSchema
from scansteward.pets.schemas import PetReadSchema
from scansteward.pets.schemas import PetUpdateSchema

router = Router(tags=["pets"])


@router.get("/", response=list[PetReadSchema])
@paginate(LimitOffsetPagination)
def get_all_pets(request: HttpRequest):
    return Pet.objects.all()


@router.get(
    "/{pet_id}/",
    response=PetReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_single_pet(request: HttpRequest, pet_id: int):
    instance: Pet = await aget_object_or_404(Pet, id=pet_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: PetReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.BAD_REQUEST: {
                "description": "Tag Already Exists",
            },
        },
    },
)
async def create_pet(request: HttpRequest, data: PetCreateSchema):
    pet_name_exists = await Pet.objects.filter(name=data.name).aexists()
    if pet_name_exists:
        raise HttpError(
            HTTPStatus.BAD_REQUEST,
            f"Tag named {data.name} already exists",
        )
    instance: Pet = await Pet.objects.acreate(
        name=data.name,
        description=data.description,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{pet_id}/",
    response={HTTPStatus.OK: PetReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_pet(request: HttpRequest, pet_id: int, data: PetUpdateSchema):
    instance: Pet = await aget_object_or_404(Pet, id=pet_id)
    if data.name is not None:
        instance.name = data.name
    if data.description is not None:
        instance.description = data.description
    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.delete(
    "/{pet_id}/",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def delete_pet(request: HttpRequest, pet_id: int):
    instance: Pet = await aget_object_or_404(Pet, id=pet_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
