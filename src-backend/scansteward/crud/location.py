from ninja import Router
from ninja.pagination import LimitOffsetPagination
from ninja.pagination import paginate

from scansteward.models import Location
from scansteward.schemas.location import LocationRead

router = Router(tags=["locations"])


@router.get("/", response=list[LocationRead])
@paginate(LimitOffsetPagination)
def get_locations():
    return Location.objects.all()
