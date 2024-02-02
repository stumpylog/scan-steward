from ninja import NinjaAPI

from image_metadata.routers import location_router
from image_metadata.routers import person_router
from image_metadata.routers import subject_router

api = NinjaAPI()
api.add_router("/person/", person_router)
api.add_router("/subject/", subject_router)
api.add_router("/location", location_router)
