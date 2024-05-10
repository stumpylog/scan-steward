import logging
from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.common.errors import Http409Error
from scansteward.models import ImageSource
from scansteward.routes.sources.schema import ImageSourceCreate
from scansteward.routes.sources.schema import ImageSourceRead
from scansteward.routes.sources.schema import ImageSourceUpdate

router = Router(tags=["sources"])

logger = logging.getLogger(__name__)


@router.get("/", response=list[ImageSourceRead])
@paginate(LimitOffsetPagination)
def get_all_sources(request: HttpRequest):
    return ImageSource.objects.all()


@router.get(
    "/{source_id}/",
    response=ImageSourceRead,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_single_source(request: HttpRequest, source_id: int):
    instance: ImageSource = await aget_object_or_404(ImageSource, id=source_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: ImageSourceRead},
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
)
async def create_source(request: HttpRequest, data: ImageSourceCreate):

    source_name_exists = await ImageSource.objects.filter(name__iexact=data.name).aexists()
    if source_name_exists:
        msg = f"Image source named {data.name} already exists"
        logger.error(msg)
        raise Http409Error(msg)

    instance: ImageSource = await ImageSource.objects.acreate(
        name=data.name,
        description=data.description,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{source_id}/",
    response={HTTPStatus.OK: ImageSourceRead},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_source(request: HttpRequest, source_id: int, data: ImageSourceUpdate):

    # Retrieve the location object from the database
    instance: ImageSource = await aget_object_or_404(ImageSource, id=source_id)

    if data.name:
        instance.name = data.name
    instance.description = data.description

    await instance.asave()

    await instance.arefresh_from_db()
    return instance
