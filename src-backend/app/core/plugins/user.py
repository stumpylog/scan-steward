from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.security.session_auth import SessionAuth
from litestar_users import LitestarUsersConfig
from litestar_users import LitestarUsersPlugin
from litestar_users.config import AuthHandlerConfig
from litestar_users.config import CurrentUserHandlerConfig
from litestar_users.config import PasswordResetHandlerConfig
from litestar_users.config import RegisterHandlerConfig
from litestar_users.config import RoleManagementHandlerConfig
from litestar_users.config import UserManagementHandlerConfig
from litestar_users.config import VerificationHandlerConfig
from litestar_users.guards import roles_accepted
from litestar_users.guards import roles_required
from litestar_users.service import BaseUserService

from app.domain.user.models import Role
from app.domain.user.models import User
from app.domain.user.schema import RoleCreateDTO
from app.domain.user.schema import RoleReadDTO
from app.domain.user.schema import RoleUpdateDTO
from app.domain.user.schema import UserReadDTO
from app.domain.user.schema import UserRegistrationDTO
from app.domain.user.schema import UserUpdateDTO


class UserService(BaseUserService[User, Role]):  # type: ignore[type-var]
    pass


litestar_users_plugin = LitestarUsersPlugin(
    config=LitestarUsersConfig(
        auth_backend_class=SessionAuth,
        session_backend_config=ServerSideSessionConfig(),
        # TODO: Fill this from settings
        secret="A" * 16,
        user_model=User,
        user_read_dto=UserReadDTO,
        user_registration_dto=UserRegistrationDTO,
        user_update_dto=UserUpdateDTO,
        role_model=Role,
        role_create_dto=RoleCreateDTO,
        role_read_dto=RoleReadDTO,
        role_update_dto=RoleUpdateDTO,
        user_service_class=UserService,
        auth_handler_config=AuthHandlerConfig(tags=["users|state"]),
        current_user_handler_config=CurrentUserHandlerConfig(tags=["users|current"]),
        password_reset_handler_config=PasswordResetHandlerConfig(tags=["users|reset"]),
        register_handler_config=RegisterHandlerConfig(tags=["users|register"]),
        role_management_handler_config=RoleManagementHandlerConfig(
            tags=["users|roles"],
            guards=[roles_accepted("administrator")],
        ),
        user_management_handler_config=UserManagementHandlerConfig(
            tags=["users|manage"],
            guards=[roles_required("administrator")],
        ),
        verification_handler_config=VerificationHandlerConfig(tags=["users|verify"]),
    ),
)
