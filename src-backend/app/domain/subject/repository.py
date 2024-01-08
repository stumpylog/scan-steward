from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from app.domain.subject.models import Subject


class SubjectRepository(SQLAlchemyAsyncRepository[Subject]):
    """
    Subject repository
    """

    model_type = Subject
