import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http400Error
from scansteward.locations.schemas import LocationCreateSchema
from scansteward.locations.schemas import LocationReadSchema
from scansteward.locations.schemas import LocationUpdateSchema
from scansteward.locations.validators import subdivision_in_country
from scansteward.models import Location

router = Router(tags=["locations"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[LocationReadSchema])
@paginate(LimitOffsetPagination)
def get_all_locations(request: HttpRequest):
    return Location.objects.all()


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
)
async def get_single_location(request: HttpRequest, location_id: int):
    instance: Location = await aget_object_or_404(Location, id=location_id)
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
                "description": "Country already exists",
            },
        },
    },
)
async def create_location(request: HttpRequest, data: LocationCreateSchema):
    country_exists = await Location.objects.filter(country=data.country_alpha_2_code).aexists()
    if country_exists:
        msg = f"Location with country {data.country_alpha_2_code.short_name} already exists"
        logger.error(msg)
        raise Http400Error(msg)

    elif data.subdivision_code and not subdivision_in_country(
        data.country_alpha_2_code,
        data.subdivision_code,
    ):
        msg = f"Subdivision {data.subdivision_code} is not in country {data.country_alpha_2_code}"
        logger.error(msg)
        raise Http400Error(msg)

    instance: Location = await Location.objects.acreate(
        country_code=data.country_alpha_2_code,
        subdivision_code=data.subdivision_code,
        city=data.city,
        sub_location=data.sub_location,
    )
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
)
async def update_location(request: HttpRequest, location_id: int, data: LocationUpdateSchema):
    # Validate that at least one field is provided to be updated
    if not any([data.country_alpha_2_code, data.subdivision_code, data.city, data.sub_location]):
        msg = "At least one of the fields must be provided"
        logger.error(msg)
        raise Http400Error(msg)

    if data.subdivision_code:
        # Check that country code is provided when subdivision code is
        if not data.country_alpha_2_code:
            msg = "Country code must be provided when the subdivision is also provided"
            logger.error(msg)
            raise Http400Error(msg)
        # Check that the provided subdivision code is in the country
        elif not subdivision_in_country(
            country_code=data.country_alpha_2_code,
            subdivision_code=data.subdivision_code,
        ):
            msg = f"Subdivision {data.subdivision_code} is not in country {data.country_alpha_2_code}"
            logger.error(msg)
            raise Http400Error(msg)

    # Retrieve the location object from the database
    instance: Location = await aget_object_or_404(Location, id=location_id)

    # Update the country
    if data.country_alpha_2_code:
        instance.country_code = str(data.country_alpha_2_code)

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
)
async def delete_location(request: HttpRequest, location_id: int):
    instance: Location = await aget_object_or_404(Location, id=location_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
