from http import HTTPStatus

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.models import Tag
from scansteward.tags.schemas import TagCreate
from scansteward.tags.schemas import TagRead
from scansteward.tags.schemas import TagTree
from scansteward.tags.schemas import TagUpdate

router = Router(tags=["tags"])


@router.get("/tree/", response=list[TagTree])
def get_tag_tree(request: HttpRequest):
    items = []
    for root_node in Tag.objects.filter(parent__isnull=True).order_by("name").prefetch_related("children"):
        tree_root = TagTree.from_orm(root_node)
        items.append(tree_root)
    return items


@router.get("/", response=list[TagRead])
@paginate(LimitOffsetPagination)
def get_tags(request: HttpRequest):
    return Tag.objects.all()


@router.get(
    "/{tag_id}",
    response=TagRead,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def get_single_tag(request: HttpRequest, tag_id: int):
    instance: Tag = await aget_object_or_404(Tag, id=tag_id)
    return instance


@router.post(
    "/",
    response={HTTPStatus.CREATED: TagRead},
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
async def create_tag(request: HttpRequest, data: TagCreate):
    tag_name_exists = await Tag.objects.filter(name=data.name).aexists()
    if tag_name_exists:
        raise HttpError(
            HTTPStatus.BAD_REQUEST,
            f"Tag named {data.name} already exists",
        )
    parent: Tag | None = None
    if data.parent_id is not None:
        parent = await aget_object_or_404(Tag, id=data.parent_id)
    instance: Tag = await Tag.objects.acreate(
        name=data.name,
        description=data.description,
        parent=parent,
    )
    return HTTPStatus.CREATED, instance


@router.patch(
    "/{tag_id}",
    response=TagRead,
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def update_tag(request: HttpRequest, tag_id: int, data: TagUpdate):
    instance: Tag = await aget_object_or_404(Tag, id=tag_id)
    if data.name is not None:
        instance.name = data.name
    if data.description is not None:
        instance.description = data.description
    if data.parent_id is not None:
        parent = await aget_object_or_404(Tag, id=data.parent_id)
        instance.parent = parent
    await instance.asave()
    await instance.arefresh_from_db()
    return instance


@router.delete(
    "/{tag_id}",
    response={HTTPStatus.NO_CONTENT: None},
    openapi_extra={
        "responses": {
            HTTPStatus.NOT_FOUND: {
                "description": "Not Found Response",
            },
        },
    },
)
async def delete_tag(request: HttpRequest, tag_id: int):
    instance: Tag = await aget_object_or_404(Tag, id=tag_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
