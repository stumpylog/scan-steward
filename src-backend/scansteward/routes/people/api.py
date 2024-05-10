import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Query
from ninja import Router
from ninja.pagination import PageNumberPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http409Error
from scansteward.models import Person
from scansteward.routes.people.schemas import PersonCreateSchema
from scansteward.routes.people.schemas import PersonNameFilter
from scansteward.routes.people.schemas import PersonReadSchema
from scansteward.routes.people.schemas import PersonUpdateSchema

router = Router(tags=["people"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[PersonReadSchema], operation_id="get_people")
@paginate(PageNumberPagination)
def get_all_people(request: HttpRequest, name_filter: Query[PersonNameFilter]):
    return Person.objects.filter(name_filter.get_filter_expression()).all()


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
    operation_id="get_person",
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
                "description": "Person Already Exists",
            },
        },
    },
    operation_id="create_person",
)
async def create_person(request: HttpRequest, data: PersonCreateSchema):
    person_name_exists = await Person.objects.filter(name__iexact=data.name).aexists()
    if person_name_exists:
        msg = f"Person named {data.name} already exists"
        logger.error(msg)
        raise Http409Error(msg)
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
    operation_id="update_person",
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
    operation_id="delete_person",
)
async def delete_person(request: HttpRequest, person_id: int):
    instance: Person = await aget_object_or_404(Person, id=person_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
