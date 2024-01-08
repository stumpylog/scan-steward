from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.models.base import AppBaseModel
from app.core.models.base import IntegerIdMixin
from app.core.models.base import TimestampMixin
from app.domain.location.models import Location
from app.domain.person.models import Person
from app.domain.subject import Subject

image_to_people_table = Table(
    "image_to_people_table",
    AppBaseModel.metadata,
    Column("image_id", ForeignKey("image.id"), primary_key=True),
    Column("person_id", ForeignKey("person.id"), primary_key=True),
)

image_to_locations_table = Table(
    "image_to_locations_table",
    AppBaseModel.metadata,
    Column("image_id", ForeignKey("image.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True),
)

image_to_subjects_table = Table(
    "image_to_subjects_table",
    AppBaseModel.metadata,
    Column("image_id", ForeignKey("image.id"), primary_key=True),
    Column("subject_id", ForeignKey("subject.id"), primary_key=True),
)


class Image(IntegerIdMixin, TimestampMixin, AppBaseModel):
    __tablename__ = "image"

    file_size: Mapped[int]
    checksum: Mapped[str] = mapped_column(String(64), unique=True, comment="blake3 hex digest")
    original_path: Mapped[str] = mapped_column(
        String(1024),
        unique=True,
        comment="Path to the original image",
    )
    thumbnail_path: Mapped[str] = mapped_column(
        String(1024),
        unique=True,
        comment="Path to the thumbnail image",
    )

    people: Mapped[list[Person]] = relationship(secondary=image_to_people_table)
    locations: Mapped[list[Location]] = relationship(secondary=image_to_locations_table)
    subjects: Mapped[list[Subject]] = relationship(secondary=image_to_subjects_table)

    @property
    def path(self) -> Path:
        return Path(self.original_path).resolve()

    @path.setter
    def path(self, path: Path | str) -> None:
        self.original_path = str(Path(path).resolve())

    @property
    def thumbnail(self) -> Path:
        return Path(self.thumbnail_path).resolve()

    @thumbnail.setter
    def thumbnail(self, path: Path | str) -> None:
        self.thumbnail_path = str(Path(path).resolve())
