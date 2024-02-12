from ninja import Router

from scansteward.people.crud import PersonViewSet

router = Router(tags=["people"])

PersonViewSet.register_routes(router)
