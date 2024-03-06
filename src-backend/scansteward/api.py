from ninja import NinjaAPI

from scansteward.albums.api import router as albums_router
from scansteward.common.renderers import ORJSONRenderer
from scansteward.images.api import router as images_router
from scansteward.locations.api import router as location_router
from scansteward.people.router import router as person_router
from scansteward.tags.api import router as tags_router

api = NinjaAPI(renderer=ORJSONRenderer())
api.add_router("/person/", person_router)
api.add_router("/location/", location_router)
api.add_router("/tag/", tags_router)
api.add_router("/image/", images_router)
api.add_router("/album/", albums_router)
