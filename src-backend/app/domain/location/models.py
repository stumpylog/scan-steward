from app.core.models.base import AppBaseModel
from app.core.models.base import IntegerIdMixin
from app.core.models.base import SimpleNamedModel
from app.core.models.base import TimestampMixin


class Location(IntegerIdMixin, TimestampMixin, SimpleNamedModel, AppBaseModel):
    __tablename__ = "location"

    def __str__(self):  # pragma: no cover
        return f"LocationModel: {self.name}"
