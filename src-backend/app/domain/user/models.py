from __future__ import annotations

from litestar_users.adapter.sqlalchemy.mixins import SQLAlchemyRoleMixin
from litestar_users.adapter.sqlalchemy.mixins import SQLAlchemyUserMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from app.models.base import AppBaseModel
from app.models.base import TimestampMixin
from app.models.base import UUIDIdBaseMixin

user_to_roles_table = Table(
    "user_to_roles_table",
    AppBaseModel.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)


class User(UUIDIdBaseMixin, TimestampMixin, SQLAlchemyUserMixin, AppBaseModel):
    __tablename__ = "user"

    roles: Mapped[list[Role]] = relationship(secondary=user_to_roles_table, lazy="selectin")


class Role(UUIDIdBaseMixin, TimestampMixin, SQLAlchemyRoleMixin, AppBaseModel):
    __tablename__ = "role"
    users: Mapped[list[User]] = relationship(
        secondary=user_to_roles_table,
        back_populates="roles",
        lazy="selectin",
    )
