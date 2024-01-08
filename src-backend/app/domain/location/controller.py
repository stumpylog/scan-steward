from collections.abc import Sequence
from typing import ClassVar

from litestar import Controller
from litestar import get
from litestar import post
from litestar import put
from litestar.di import Provide
from litestar.exceptions import NotFoundException
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset

from app.core.providers import provide_limit_offset_pagination
from app.domain.location.models import Location as LocationModel
from app.domain.location.providers import provide_locations_repo
from app.domain.location.repository import LocationRepository
from app.domain.location.schema import LocationCreateDTO
from app.domain.location.schema import LocationReadDTO
from app.domain.location.schema import LocationUpdateDTO


class LocationController(Controller):
    path = "/location/"

    tags: Sequence[str] = ["location"]

    dependencies: ClassVar[dict[str, Provide]] = {
        "locations_repo": Provide(provide_locations_repo),
    }

    @get(
        dependencies={
            "limit_offset": Provide(provide_limit_offset_pagination),
        },
        summary="List all locations",
    )
    async def get_locations(
        self,
        locations_repo: LocationRepository,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[LocationModel]:
        """
        List locations
        """
        results, total = await locations_repo.list_and_count(limit_offset)
        return OffsetPagination[LocationModel](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @get(
        "{location_id:int}",
        summary="Get a single location",
        raises=[NotFoundException],
    )
    async def get_single_location(
        self,
        locations_repo: LocationRepository,
        location_id: int,
    ) -> LocationModel:
        """
        Get single location
        """
        obj = await locations_repo.get_one_or_none(id=location_id)
        if obj is None:
            raise NotFoundException(detail=f"Location with ID {location_id} not found")
        return obj

    @post(dto=LocationCreateDTO, return_dto=LocationReadDTO, summary="Creates a new Location")
    async def create_location(
        self,
        locations_repo: LocationRepository,
        data: LocationModel,
    ) -> LocationModel:
        """
        Creates a Location
        """
        obj = await locations_repo.add(data)
        await locations_repo.session.commit()
        return obj

    @put(
        "{location_id:int}/",
        dto=LocationUpdateDTO,
        return_dto=LocationReadDTO,
        summary="Updates a single location",
        raises=[NotFoundException],
    )
    async def update_location(
        self,
        locations_repo: LocationRepository,
        location_id: int,
        data: LocationModel,
    ) -> LocationModel:
        """
        Updates a location
        """
        obj = await locations_repo.get_one_or_none(id=location_id)
        if obj is None:
            raise NotFoundException(detail=f"Location with ID {location_id} not found")
        data.id = obj.id
        await locations_repo.update(data, ["name"])
        await locations_repo.session.commit()
        obj = await locations_repo.get(location_id)
        return obj
