from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTOConfig
from litestar.contrib.pydantic import PydanticDTO
from pydantic import BaseModel
from pydantic import EmailStr

from app.models.user import Role
from app.models.user import User


class RoleCreateDTO(SQLAlchemyDTO[Role]):
    config = SQLAlchemyDTOConfig(exclude={"id", "created_at", "updated_at", "users"})


class RoleReadDTO(SQLAlchemyDTO[Role]):
    config = SQLAlchemyDTOConfig(exclude={"users"})


class RoleUpdateDTO(SQLAlchemyDTO[Role]):
    config = SQLAlchemyDTOConfig(exclude={"id", "users"}, partial=True)


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    title: str


class UserRegistrationDTO(PydanticDTO[UserRegistrationSchema]):
    """
    User registration DTO
    """


class UserReadDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={"password_hash"})


class UserUpdateDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "is_active", "is_verified", "roles"},
        partial=True,
    )
