from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from scansteward.images.schemas import BoundingBox
from scansteward.images.schemas import PersonWithBox
from scansteward.people.schemas import PersonReadSchema


class TimestampMixin(models.Model):
    """
    Mixin class to provide created_at and updated_at columns in UTC
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleNamedModel(models.Model):
    """
    Basic model which provides a short name column and longer description column
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)

    description = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    class Meta:
        abstract = True


class Tag(TimestampMixin, models.Model):
    """
    Holds the information about a Tag, roughly a tag, in a tree structure,
    whose structure makes sense to the user
    """

    name = models.CharField(max_length=100, db_index=True)

    description = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    applied = models.BooleanField(default=False)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
    )

    class Meta:
        constraints: Sequence = [
            models.UniqueConstraint(fields=["name", "parent"], name="name-to-parent"),
        ]


class Person(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a single person
    """


class FaceInImage(TimestampMixin, models.Model):
    """
    Holds information for a face in an image, ideally tied to a Person
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="images",
        help_text="Person is in this Image at the given location",
        null=True,
    )
    image = models.ForeignKey(
        "Image",
        on_delete=models.CASCADE,
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

    exclude_from_training = models.BooleanField(
        default=False,
        help_text="For future growth, do not use this box for facial recognition training",
    )

    @property
    def name(self) -> str:
        if self.person:
            return self.person.name
        return "Unknown"


class Album(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds multiple Images in an ordered form, with a name and optional description
    """

    images = models.ManyToManyField(
        "Image",
        through="ImageInAlbum",
        related_name="albums",
    )

    def image_ids(self) -> list[int]:
        return self.images.order_by("imageinalbum__sort_order").values_list("id", flat=True)


class ImageInAlbum(TimestampMixin, models.Model):
    """
    Through model to hold the ordering for an album
    """

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        null=True,
    )
    image = models.ForeignKey(
        "Image",
        on_delete=models.CASCADE,
    )

    sort_order = models.PositiveBigIntegerField(verbose_name="Order of this image in the album")

    class Meta:
        ordering = ["sort_order"]  # noqa: RUF012
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["sort_order", "album"], name="sorting-to-album"),
        ]


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

    file_size = models.PositiveBigIntegerField(
        verbose_name="file size in bytes",
        help_text="Size of the original file in bytes",
    )

    source = models.CharField(
        max_length=100,
        verbose_name="Source of the image",
        help_text="The string source of the image, example a box or carousel identifier",
        blank=True,
        null=True,
    )

    original = models.CharField(
        max_length=1024,
        unique=True,
        verbose_name="Path to the original image",
    )

    people = models.ManyToManyField(
        Person,
        through=FaceInImage,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="images",
    )

    @property
    def original_path(self) -> Path:
        return Path(self.original).resolve()

    @original_path.setter
    def original_path(self, path: Path | str) -> None:
        self.original = str(Path(path).resolve())

    @property
    def thumbnail_path(self) -> Path:
        if TYPE_CHECKING:
            assert hasattr(settings, "THUMBNAIL_DIR")
            assert isinstance(settings.THUMBNAIL_DIR, Path)
        return (settings.THUMBNAIL_DIR / f"{self.pk:010}").with_suffix(".webp").resolve()

    @property
    def full_size_path(self) -> Path:
        if TYPE_CHECKING:
            assert isinstance(settings.FULL_SIZE_DIR, Path)
        return (settings.FULL_SIZE_DIR / f"{self.pk:010}").with_suffix(".webp").resolve()

    @property
    def face_boxes(self) -> list[PersonWithBox]:
        boxes = []
        for person in self.people.all():
            bounding_box = FaceInImage.objects.filter(image=self, person=person).first()
            if TYPE_CHECKING:
                assert bounding_box is not None
            boxes.append(
                PersonWithBox(
                    person=PersonReadSchema.from_orm(person),
                    box=BoundingBox(
                        center_x=bounding_box.center_x,
                        center_y=bounding_box.center_y,
                        height=bounding_box.height,
                        width=bounding_box.width,
                    ),
                ),
            )
        return boxes
