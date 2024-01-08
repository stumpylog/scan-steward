from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig

from app.domain.subject.models import Subject as SubjectModel


class SubjectCreateDTO(SQLAlchemyDTO[SubjectModel]):
    config = SQLAlchemyDTOConfig(include={"name"})


class SubjectReadDTO(SQLAlchemyDTO[SubjectModel]):
    pass


class SubjectUpdateDTO(SubjectCreateDTO):
    config = SQLAlchemyDTOConfig(exclude={"id", "created_at", "updated_at"}, partial=True)
