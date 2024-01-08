from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.subject.repository import SubjectRepository


async def provide_subjects_repo(db_session: AsyncSession) -> SubjectRepository:
    """
    This provides the default Subject repository
    """
    return SubjectRepository(session=db_session)
