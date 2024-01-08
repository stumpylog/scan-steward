from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from app.api import CustomOpenAPIController
from app.api import api_router
from app.core.plugins.database import sql_alchemy_plugin

# from app.plugins.user import litestar_users_plugin # noqa: ERA001

app = Litestar(
    plugins=[
        # litestar_users_plugin,
        sql_alchemy_plugin,
    ],
    route_handlers=[api_router],
    openapi_config=OpenAPIConfig(
        title="Scan Steward",
        version="0.1.0",
        openapi_controller=CustomOpenAPIController,
    ),
    debug=True,
)
