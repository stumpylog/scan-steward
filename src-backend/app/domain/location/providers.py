from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.location.repository import LocationRepository


async def provide_locations_repo(db_session: AsyncSession) -> LocationRepository:
    """
    This provides the default Locations repository
    """
    return LocationRepository(session=db_session)
