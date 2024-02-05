from __future__ import annotations

from pathlib import Path

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from image_metadata.models import Person
from scansteward.models import TimestampMixin


class PersonInImage(TimestampMixin, models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="faces",
        help_text="Person is in this Image at the given location",
    )
    image = models.ForeignKey(
        "Image",
        on_delete=models.CASCADE,
        related_name="faces",
        help_text="Person is in this Image at the given location",
    )

    # bounding box around face
    # These are stored as relative values, with 1.0 being the most
    center_x = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    center_y = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    height = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    width = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )

    exclude_from_training = models.BooleanField(default=False)

    @property
    def name(self) -> str:
        return self.person.name


class Image(TimestampMixin, models.Model):
    """
    Holds the information about an Image
    """

    checksum = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="blake3 hex digest",
        help_text="The BLAKE3 checksum of the original file",
    )
    original_path = models.CharField(max_length=1024, unique=True, verbose_name="Path to the original image")
    webp_path = models.CharField(
        max_length=1024,
        unique=True,
        verbose_name="full size WebP of the original",
    )
    thumbnail_path = models.CharField(max_length=1024, unique=True, verbose_name="thumbnail image in WebP")

    people = models.ManyToManyField(Person, through=PersonInImage, related_name="image")

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
