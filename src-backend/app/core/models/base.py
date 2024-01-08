from advanced_alchemy.base import AuditColumns
from advanced_alchemy.base import BigIntPrimaryKey
from advanced_alchemy.base import UUIDPrimaryKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import mapped_column


class AppBaseModel(DeclarativeBase):
    """
    The base model any database model must inherit from
    """


@declarative_mixin
class IntegerIdMixin(BigIntPrimaryKey):
    """
    Mixin class to provide a big integer primary key
    """


@declarative_mixin
class UUIDIdBaseMixin(UUIDPrimaryKey):
    """
    Mixin class to provide a UUID primary key
    """


@declarative_mixin
class TimestampMixin(AuditColumns):
    """
    Mixin class to provide created_at and updated_at columns in UTC
    """


@declarative_mixin
class SimpleNamedModel:
    """
    Basic model which provides a short name column and longer description column
    """

    name: Mapped[str] = mapped_column(String(100), unique=True)

    description: Mapped[str] = mapped_column(String(1024), nullable=True, default=None)
