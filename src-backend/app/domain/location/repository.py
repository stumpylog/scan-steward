from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from app.domain.location.models import Location


class LocationRepository(SQLAlchemyAsyncRepository[Location]):
    """
    Location repository
    """

    model_type = Location
