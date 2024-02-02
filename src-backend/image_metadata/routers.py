from ninja import Router

from image_metadata.crud import LocationViewSet
from image_metadata.crud import PersonViewSet
from image_metadata.crud import SubjectViewSet

location_router = Router(tags=["locations"])
subject_router = Router(tags=["subjects"])
person_router = Router(tags=["people"])

LocationViewSet.register_routes(location_router)
SubjectViewSet.register_routes(subject_router)
PersonViewSet.register_routes(person_router)
