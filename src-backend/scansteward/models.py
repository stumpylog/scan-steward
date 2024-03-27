from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from scansteward.routes.pets.schemas import PetReadSchema

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from scansteward.imageops.models import RotationEnum
from scansteward.routes.images.schemas import BoundingBox
from scansteward.routes.images.schemas import PersonWithBox


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


class Pet(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a single person
    """

    class PetTypeChoices(models.TextChoices):
        CAT = "cat"
        DOG = "dog"
        HORSE = "horse"

    pet_type = models.CharField(
        max_length=10,
        choices=PetTypeChoices.choices,
        null=True,
        blank=True,
        help_text="The type of pet this is",
    )


class RoughDate(TimestampMixin, models.Model):
    """
    The rough date of the image
    """

    date = models.DateField(unique=True, help_text="The date of the image, maybe not exact")

    month_valid = models.BooleanField(default=False, help_text="Is the month of this date valid?")
    day_valid = models.BooleanField(default=False, help_text="Is the day of this date valid?")

    class Meta:
        ordering: Sequence = ["date"]
        constraints: Sequence = [
            models.UniqueConstraint(
                fields=["date", "month_valid", "day_valid"],
                name="unique-date",
            ),
        ]


class AbstractBoxInImage(TimestampMixin, models.Model):
    """
    Holds information for a bounding box in an image, ideally tied to a Person or Per
    """

    image = models.ForeignKey(
        "Image",
        on_delete=models.CASCADE,
        help_text="A Thing is in this Image at the given location",
    )

    # bounding box around a region
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

    class Meta:
        abstract = True


class PersonInImage(AbstractBoxInImage):
    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="images",
        help_text="Person is in this Image at the given location",
        null=True,
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


class PetInImage(AbstractBoxInImage):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.SET_NULL,
        related_name="images",
        help_text="Pet is in this Image at the given location",
        null=True,
    )

    @property
    def name(self) -> str:
        if self.pet:
            return self.pet.name
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
        ordering: Sequence = ["sort_order"]
        constraints: Sequence = [
            models.UniqueConstraint(fields=["sort_order", "album"], name="sorting-to-album"),
        ]


class Location(TimestampMixin, models.Model):
    """
    Holds the information about a Location where an image was.

    As much information should be filled in as possible, at least the country is required
    """

    country_code = models.CharField(
        max_length=4,
        db_index=True,
        help_text="Country code in ISO 3166-1 alpha 2 format",
    )
    subdivision_code = models.CharField(
        max_length=12,  # Longest subdivision in the world is 6 characters, double that
        db_index=True,
        null=True,
        blank=True,
        help_text="State, province or subdivision ISO 3166-2 alpha 2 format",
    )
    city = models.CharField(max_length=255, db_index=True, null=True, blank=True, help_text="City or town")
    sub_location = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text="Detailed location within a city or Town",
    )

    class Meta:
        ordering: Sequence = ["country_code", "subdivision_code", "city", "sub_location"]
        constraints: Sequence = [
            models.UniqueConstraint(
                fields=["country_code", "subdivision_code", "city", "sub_location"],
                name="unique-location",
            ),
        ]


class Image(TimestampMixin, models.Model):
    """
    Holds the information about an Image
    """

    class OrientationChoices(models.IntegerChoices):
        HORIZONTAL = RotationEnum.HORIZONTAL.value
        MIRROR_HORIZONTAL = RotationEnum.MIRROR_HORIZONTAL.value
        ROTATE_180 = RotationEnum.ROTATE_180.value
        MIRROR_VERTICAL = RotationEnum.MIRROR_VERTICAL.value
        MIRROR_HORIZONTAL_AND_ROTATE_270_CW = RotationEnum.MIRROR_HORIZONTAL_AND_ROTATE_270_CW.value
        ROTATE_90_CW = RotationEnum.ROTATE_90_CW.value
        MIRROR_HORIZONTAL_AND_ROTATE_90_CW = RotationEnum.MIRROR_HORIZONTAL_AND_ROTATE_90_CW.value
        ROTATE_270_CW = RotationEnum.ROTATE_270_CW.value

    checksum = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="blake3 hex digest",
        help_text="The BLAKE3 checksum of the original file",
    )

    phash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="perceptual average hash of the image",
        help_text="The pHash (average) of the original file",
    )

    file_size = models.PositiveBigIntegerField(
        verbose_name="file size in bytes",
        help_text="Size of the original file in bytes",
    )

    orientation = models.SmallIntegerField(
        choices=OrientationChoices.choices,
        default=OrientationChoices.HORIZONTAL,
        help_text="MWG Orientation flag",
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="images",
        help_text="Location where the image was taken, with as much refinement as possible",
    )

    date = models.ForeignKey(
        RoughDate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="images",
        help_text="RoughDate when the image was taken, with as much refinement as possible",
    )

    description = models.TextField(null=True, blank=True, help_text="MWG Description tag")

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

    is_dirty = models.BooleanField(
        default=False,
        help_text="The metadata is dirty and needs to be synced to the file",
    )

    people = models.ManyToManyField(
        Person,
        through=PersonInImage,
    )

    pets = models.ManyToManyField(
        Pet,
        through=PetInImage,
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
        return (settings.THUMBNAIL_DIR / self.image_fs_id).with_suffix(".webp").resolve()

    @property
    def full_size_path(self) -> Path:
        if TYPE_CHECKING:
            assert isinstance(settings.FULL_SIZE_DIR, Path)
        return (settings.FULL_SIZE_DIR / self.image_fs_id).with_suffix(".webp").resolve()

    @property
    def face_boxes(self) -> list[PersonWithBox]:
        boxes = []
        for person in self.people.all():
            bounding_box = PersonInImage.objects.filter(image=self, person=person).first()
            if TYPE_CHECKING:
                assert bounding_box is not None
            boxes.append(
                PersonWithBox(
                    person_id=person.pk,
                    box=BoundingBox(
                        center_x=bounding_box.center_x,
                        center_y=bounding_box.center_y,
                        height=bounding_box.height,
                        width=bounding_box.width,
                    ),
                ),
            )
        return boxes

    @property
    def pet_boxes(self) -> list[PetReadSchema]:
        boxes = []
        for pet in self.pets.all():
            bounding_box = PetInImage.objects.filter(image=self, pet=pet).first()
            if TYPE_CHECKING:
                assert bounding_box is not None
            boxes.append(
                PersonWithBox(
                    pet_id=pet.pk,
                    box=BoundingBox(
                        center_x=bounding_box.center_x,
                        center_y=bounding_box.center_y,
                        height=bounding_box.height,
                        width=bounding_box.width,
                    ),
                ),
            )
        return boxes

    @property
    def image_fs_id(self) -> str:
        return f"{self.pk:010}"
