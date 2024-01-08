from app.core.models.base import AppBaseModel
from app.core.models.base import IntegerIdMixin
from app.core.models.base import SimpleNamedModel
from app.core.models.base import TimestampMixin


class Subject(IntegerIdMixin, TimestampMixin, SimpleNamedModel, AppBaseModel):
    __tablename__ = "subject"
