import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http400Error
from scansteward.common.errors import Http409Error
from scansteward.models import RoughDate
from scansteward.routes.rough_dates.schema import RoughDateCreateSchema
from scansteward.routes.rough_dates.schema import RoughDateReadSchema
from scansteward.routes.rough_dates.schema import RoughDateUpdateSchema

router = Router(tags=["dates"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[RoughDateReadSchema])
@paginate(LimitOffsetPagination)
def get_all_dates(request: HttpRequest):
    return RoughDate.objects.all()


@router.get(
    "/{date_id}/",
    response=RoughDateReadSchema,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_single_rough_date(request: HttpRequest, date_id: int):
    instance: RoughDate = await aget_object_or_404(RoughDate, id=date_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: RoughDateReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
            HTTPStatus.BAD_REQUEST: {
                "description": "Date Already Exists",
            },
        },
    },
)
async def create_rough_date(request: HttpRequest, data: RoughDateCreateSchema):
    rough_date_exists = await RoughDate.objects.filter(
        date=data.date,
        month_valid=data.month_valid,
        day_valid=data.day_valid,
    ).aexists()
    if rough_date_exists:
        msg = f"Date at {data.date} already exists"
        logger.error(msg)
        raise Http409Error(msg)
    instance: RoughDate = await RoughDate.objects.acreate(
        date=data.date,
        month_valid=data.month_valid,
        day_valid=data.day_valid,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{date_id}/",
    response={HTTPStatus.OK: RoughDateReadSchema},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_rough_date(request: HttpRequest, date_id: int, data: RoughDateUpdateSchema):
    if not any([data.date, data.month_valid, data.day_valid]):
        msg = "At least one field must be updated"
        logger.error(msg)
        raise Http400Error(msg)
    instance: RoughDate = await aget_object_or_404(RoughDate, id=date_id)
    if data.date is not None:
        instance.date = data.date
    if data.month_valid is not None:
        instance.month_valid = data.month_valid
    if data.day_valid is not None:
        instance.day_valid = data.day_valid
    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.delete(
    "/{date_id}/",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def delete_rough_date(request: HttpRequest, date_id: int):
    instance: RoughDate = await aget_object_or_404(RoughDate, id=date_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
