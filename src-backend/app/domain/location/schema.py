from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig

from app.domain.location.models import Location as LocationModel


class LocationCreateDTO(SQLAlchemyDTO[LocationModel]):
    config = SQLAlchemyDTOConfig(include={"name"})


class LocationReadDTO(SQLAlchemyDTO[LocationModel]):
    pass


class LocationUpdateDTO(LocationCreateDTO):
    config = SQLAlchemyDTOConfig(exclude={"id", "created_at", "updated_at"}, partial=True)
