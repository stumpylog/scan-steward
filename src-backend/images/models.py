from __future__ import annotations

from pathlib import Path

from django.db import models

from image_metadata.models import Person
from scansteward.models import TimestampMixin


class PersonInImage(TimestampMixin, models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="faces")
    image = models.ForeignKey("Image", on_delete=models.CASCADE, related_name="faces")

    # bounding box around face
    center_x = models.PositiveIntegerField()
    center_y = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()

    exclude_from_training = models.BooleanField(default=False)

    @property
    def name(self) -> str:
        return self.person.name


class Image(TimestampMixin, models.Model):
    """
    Holds the information about an Image
    """

    checksum = models.CharField(max_length=64, unique=True, verbose_name="blake3 hex digest")
    original_path = models.CharField(max_length=1024, unique=True, verbose_name="Path to the original image")
    webp_path = models.CharField(
        max_length=1024,
        unique=True,
        verbose_name="Path to the full size, but WebP mage",
    )
    thumbnail_path = models.CharField(max_length=1024, unique=True, verbose_name="Path to a thumbnail image")

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

    @property
    def webp(self) -> Path:
        return Path(self.webp_path).resolve()

    @webp.setter
    def webp(self, path: Path | str) -> None:
        self.webp_path = str(Path(path).resolve())
