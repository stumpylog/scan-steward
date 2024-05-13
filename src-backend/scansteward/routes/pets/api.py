import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http409Error
from scansteward.models import Pet
from scansteward.routes.pets.schemas import PetCreateSchema
from scansteward.routes.pets.schemas import PetReadSchema
from scansteward.routes.pets.schemas import PetUpdateSchema

router = Router(tags=["pets"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[PetReadSchema], operation_id="get_pets")
@paginate(PageNumberPagination)
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
    operation_id="get_single_pet",
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
    operation_id="create_pet",
)
async def create_pet(request: HttpRequest, data: PetCreateSchema):
    pet_name_exists = await Pet.objects.filter(name__iexact=data.name).aexists()
    if pet_name_exists:
        msg = f"Pet named {data.name} already exists"
        logger.warning(msg)
        raise Http409Error(msg)
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
    operation_id="update_pet",
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
    operation_id="delete_pet",
)
async def delete_pet(request: HttpRequest, pet_id: int):
    instance: Pet = await aget_object_or_404(Pet, id=pet_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
