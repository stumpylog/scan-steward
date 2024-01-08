from litestar import Router
from litestar.openapi import OpenAPIController

from app.domain.location.controller import LocationController
from app.domain.subject.controller import SubjectController

api_router = Router(path="/api/v1/", route_handlers=[LocationController, SubjectController])


class CustomOpenAPIController(OpenAPIController):
    """
    Overrides the path so it will show up under the proper version
    """

    path = "/api/v1/schema/"
