from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.models import Person
from scansteward.people.schemas import PersonCreateSchema
from scansteward.people.schemas import PersonReadSchema
from scansteward.people.schemas import PersonUpdateSchema

router = Router(tags=["people"])


@router.get("/", response=list[PersonReadSchema])
@paginate(LimitOffsetPagination)
def get_all_people(request: HttpRequest):
    return Person.objects.all()


@router.get(
    "/{person_id}/",
    response=PersonReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_single_person(request: HttpRequest, person_id: int):
    instance: Person = await aget_object_or_404(Person, id=person_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: PersonReadSchema},
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
async def create_person(request: HttpRequest, data: PersonCreateSchema):
    person_name_exists = await Person.objects.filter(name=data.name).aexists()
    if person_name_exists:
        raise HttpError(
            HTTPStatus.BAD_REQUEST,
            f"Tag named {data.name} already exists",
        )
    instance: Person = await Person.objects.acreate(
        name=data.name,
        description=data.description,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{person_id}/",
    response={HTTPStatus.OK: PersonReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_person(request: HttpRequest, person_id: int, data: PersonUpdateSchema):
    instance: Person = await aget_object_or_404(Person, id=person_id)
    if data.name is not None:
        instance.name = data.name
    if data.description is not None:
        instance.description = data.description
    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.delete(
    "/{person_id}/",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def delete_person(request: HttpRequest, person_id: int):
    instance: Person = await aget_object_or_404(Person, id=person_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
