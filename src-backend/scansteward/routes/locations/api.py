import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http400Error
from scansteward.common.errors import Http409Error
from scansteward.models import RoughLocation
from scansteward.routes.locations.schemas import LocationCreateSchema
from scansteward.routes.locations.schemas import LocationReadSchema
from scansteward.routes.locations.schemas import LocationUpdateSchema
from scansteward.routes.locations.utils import subdivision_in_country

router = Router(tags=["locations"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[LocationReadSchema], operation_id="get_locations")
@paginate(LimitOffsetPagination)
def get_all_locations(request: HttpRequest):
    return RoughLocation.objects.all()


@router.get(
    "/{location_id}/",
    response=LocationReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="get_location",
)
async def get_single_location(request: HttpRequest, location_id: int):
    instance: RoughLocation = await aget_object_or_404(RoughLocation, id=location_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: LocationReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.BAD_REQUEST: {
                "description": "Subdivision provided without country",
            },
            HTTPStatus.CONFLICT: {
                "description": "RoughLocation already exists",
            },
        },
    },
    operation_id="create_location",
)
async def create_location(request: HttpRequest, data: LocationCreateSchema):
    if data.subdivision_code and not subdivision_in_country(
        data.country_code,
        data.subdivision_code,
    ):
        msg = f"Subdivision {data.subdivision_code} is not in country {data.country_code}"
        logger.error(msg)
        raise Http400Error(msg)

    instance, created = await RoughLocation.objects.aget_or_create(
        country_code=data.country_code,
        subdivision_code=data.subdivision_code,
        city=data.city,
        sub_location=data.sub_location,
    )
    if not created:
        msg = "RoughLocation with provided fields already exists"
        logger.error(msg)
        raise Http409Error(msg)

    return HTTPStatus.CREATED, instance


@router.patch(
    "/{location_id}/",
    response={HTTPStatus.OK: LocationReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="update_location",
)
async def update_location(request: HttpRequest, location_id: int, data: LocationUpdateSchema):
    # Validate that at least one field is provided to be updated
    if not any([data.country_code, data.subdivision_code, data.city, data.sub_location]):
        msg = "At least one of the fields must be provided"
        logger.error(msg)
        raise Http400Error(msg)

    # Retrieve the location object from the database
    instance: RoughLocation = await aget_object_or_404(RoughLocation, id=location_id)

    # Update the country
    if data.country_code:
        instance.country_code = str(data.country_code)

    # Update the subdivision/state/province value
    if data.subdivision_code:
        instance.subdivision_code = data.subdivision_code

    instance.city = data.city
    instance.sub_location = data.sub_location

    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.delete(
    "/{location_id}/",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
    operation_id="delete_location",
)
async def delete_location(request: HttpRequest, location_id: int):
    instance: RoughLocation = await aget_object_or_404(RoughLocation, id=location_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
