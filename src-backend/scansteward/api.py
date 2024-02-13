from ninja import NinjaAPI

from scansteward.locations.api import router as location_router
from scansteward.people.router import router as person_router
from scansteward.tags.api import router as tags_router

api = NinjaAPI()
api.add_router("/person/", person_router)
api.add_router("/location/", location_router)
api.add_router("/tag/", tags_router)
