from http import HTTPStatus
from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.shortcuts import aget_object_or_404
from ninja import Router
from ninja.errors import HttpError

from scansteward.locations.schemas import LocationCreate
from scansteward.locations.schemas import LocationRead
from scansteward.locations.schemas import LocationTree
from scansteward.locations.schemas import LocationUpdate
from scansteward.models import Location

router = Router(tags=["locations"])


@router.get("/", response=list[LocationTree])
def get_locations(request: HttpRequest):
    items = []
    for root_node in Location.objects.filter(parent__isnull=True).prefetch_related("children"):
        tree_root = LocationTree.from_orm(root_node)
        items.append(tree_root)
    return items


@router.post("/", response=LocationRead)
async def create_location(request: HttpRequest, data: LocationCreate):
    location_name_exists = await Location.objects.filter(name=data.name).aexists()
    if location_name_exists:
        raise HttpError(HTTPStatus.BAD_REQUEST, f"Location named {data.name} already exists")
    parent: Location | None = None
    if data.parent_id is not None:
        parent = await aget_object_or_404(Location, id=data.parent_id)
    instance: Location = await Location.objects.acreate(
        name=data.name,
        description=data.description,
        parent=parent,
    )
    return instance


@router.patch("/", response=LocationRead)
async def update_location(request: HttpRequest, data: LocationUpdate):
    instance: Location = await aget_object_or_404(Location, id=data.id)
    instance.name = data.name
    instance.description = data.description
    parent: Location | None = None
    if data.parent_id is not None:
        parent = await aget_object_or_404(Location, id=data.parent_id)
        if TYPE_CHECKING:
            assert isinstance(parent, Location)
    instance.parent = parent
    await instance.asave()
    return instance


@router.delete("/{location_id}", response={204: None})
async def delete_location(request: HttpRequest, location_id: int):
    instance: Location = await aget_object_or_404(Location, id=location_id)
    await instance.adelete()
    return HTTPStatus.NO_CONTENT, None
