from pathlib import Path

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


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

    description = models.CharField(max_length=1024, null=True, default=None, db_index=True)

    class Meta:
        abstract = True


class Tag(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a Tag, roughly a tag
    """

    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children")


class Location(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a Location, some rough idea of a location, not actual GPS
    """

    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True)

    @property
    def parent_id(self) -> int | None:
        if self.parent:
            return self.parent.id
        return None


class Person(SimpleNamedModel, TimestampMixin, models.Model):
    """
    Holds the information about a single person
    """


class PersonCreateImage(TimestampMixin, models.Model):
    """
    Holds information for a face in an image, ideally tied to a Person
    """

    person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        related_name="faces",
        help_text="Person is in this Image at the given location",
        null=True,
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
        if self.person:
            return self.person.name
        return "Unknown"


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
    original = models.CharField(max_length=1024, unique=True, verbose_name="Path to the original image")
    full_size = models.CharField(
        max_length=1024,
        unique=True,
        verbose_name="full size WebP of the original",
    )
    thumbnail = models.CharField(max_length=1024, unique=True, verbose_name="thumbnail image in WebP")

    people = models.ManyToManyField(Person, through=PersonCreateImage, related_name="image")

    @property
    def original_path(self) -> Path:
        return Path(self.original).resolve()

    @original_path.setter
    def original_path(self, path: Path | str) -> None:
        self.original = str(Path(path).resolve())

    @property
    def thumbnail_path(self) -> Path:
        return Path(self.thumbnail).resolve()

    @thumbnail_path.setter
    def thumbnail_path(self, path: Path | str) -> None:
        self.thumbnail = str(Path(path).resolve())

    @property
    def full_size_path(self) -> Path:
        return Path(self.full_size).resolve()

    @full_size_path.setter
    def full_size_path(self, path: Path | str) -> None:
        self.full_size = str(Path(path).resolve())
