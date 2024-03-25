from ninja import NinjaAPI

from scansteward.common.parser import OrjsonParser
from scansteward.common.renderer import OrjsonRenderer
from scansteward.routes.albums.api import router as albums_router
from scansteward.routes.images.api import router as images_router
from scansteward.routes.locations.api import router as locations_router
from scansteward.routes.people.api import router as person_router
from scansteward.routes.pets.api import router as pets_router
from scansteward.routes.tags.api import router as tags_router

api = NinjaAPI(title="ScanSteward API", renderer=OrjsonRenderer(), parser=OrjsonParser())
api.add_router("/person/", person_router)
api.add_router("/tag/", tags_router)
api.add_router("/image/", images_router)
api.add_router("/album/", albums_router)
api.add_router("/pet/", pets_router)
api.add_router("/location/", locations_router)
