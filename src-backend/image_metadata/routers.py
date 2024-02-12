from ninja import Router

from image_metadata.crud import LocationViewSet
from image_metadata.crud import TagViewSet

location_router = Router(tags=["locations"])
Tag_router = Router(tags=["Tags"])
person_router = Router(tags=["people"])

LocationViewSet.register_routes(location_router)
TagViewSet.register_routes(Tag_router)
