from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import PersonRepository


async def provide_people_repo(db_session: AsyncSession) -> PersonRepository:
    """
    This provides the default People repository
    """
    return PersonRepository(session=db_session)
