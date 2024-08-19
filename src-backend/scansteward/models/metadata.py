from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from scansteward.models.image import Image  # noqa: F401


from django.db import models
from simpleiso3166.countries import Country

from scansteward.models.abstract import AbstractBoxInImage
from scansteward.models.abstract import AbstractSimpleNamedModel
from scansteward.models.abstract import AbstractTimestampMixin


class Tag(AbstractTimestampMixin, models.Model):
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

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.applied})"

    def __repr__(self) -> str:
        return f"Tag: {self!s}"

    class Meta:
        constraints: Sequence = [
            models.UniqueConstraint(fields=["name", "parent"], name="name-to-parent"),
        ]


class TagOnImage(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, help_text="Tag is on this Image")

    image = models.ForeignKey(
        "Image",
        on_delete=models.CASCADE,
        help_text="A Tag is on this Image at the given location",
    )

    applied = models.BooleanField(default=False, help_text="This tag is applied to this image")


class Person(AbstractSimpleNamedModel, AbstractTimestampMixin, models.Model):
    """
    Holds the information about a single person
    """


class PersonInImage(AbstractBoxInImage):
    person = models.ForeignKey(
        Person,
        # TODO: This would need to update if we allow boxes without a name/person attached
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Person is in this Image at the given location",
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


class Pet(AbstractSimpleNamedModel, AbstractTimestampMixin, models.Model):
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


class PetInImage(AbstractBoxInImage):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Pet is in this Image at the given location",
        null=True,
    )

    @property
    def name(self) -> str:
        if self.pet:
            return self.pet.name
        return "Unknown"


class ImageSource(AbstractTimestampMixin, models.Model):
    """
    Holds multiple Images in an ordered form, with a name and optional description
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)

    description = models.TextField(
        null=True,
        blank=True,
        default=None,
        help_text="A description of this source, rendered as markdown",
    )


class RoughDate(AbstractTimestampMixin, models.Model):
    """
    The rough date of the image
    """

    date = models.DateField(
        unique=True,
        help_text="The date of the image, maybe not exact",
    )

    month_valid = models.BooleanField(
        default=False,
        help_text="Is the month of this date valid?",
    )
    day_valid = models.BooleanField(
        default=False,
        help_text="Is the day of this date valid?",
    )

    def __str__(self) -> str:
        year = self.date.year
        month = self.date.month if self.month_valid else "MM"
        day = self.date.day if self.day_valid else "DD"
        return f"{year}-{month}-{day}"

    def __repr__(self) -> str:
        return f"RoughDate: {self!s}"

    class Meta:
        ordering: Sequence = ["date"]
        constraints: Sequence = [
            models.CheckConstraint(
                condition=(models.Q(day_valid=False) | ~models.Q(month_valid=False)),
                name="invalid-month-day-combo",
            ),
            models.UniqueConstraint(
                fields=["date", "month_valid", "day_valid"],
                name="unique-date",
            ),
        ]


class RoughLocation(AbstractTimestampMixin, models.Model):
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
    city = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text="City or town",
    )
    sub_location = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        help_text="Detailed location within a city or Town",
    )

    class Meta:
        ordering: Sequence = [
            "country_code",
            "subdivision_code",
            "city",
            "sub_location",
        ]
        constraints: Sequence = [
            models.UniqueConstraint(
                fields=["country_code", "subdivision_code", "city", "sub_location"],
                name="unique-location",
            ),
        ]

    def __str__(self) -> str:
        country = Country.from_alpha2(self.country_code)  # type: ignore[arg-type]
        if TYPE_CHECKING:
            assert isinstance(country, Country)
        value = f"Country: {country.common_name or country.name}"
        if self.subdivision_code:
            subdivision_name = country.get_subdivision_name(self.subdivision_code)  # type: ignore[arg-type]
            if TYPE_CHECKING:
                assert isinstance(subdivision_name, str)
            value = f"{value} - State: {subdivision_name}"
        if self.city:
            value = f"{value} - City: {self.city}"
        if self.sub_location:
            value = f"{value} - Location: {self.sub_location}"
        return value

    def __repr__(self) -> str:
        return f"RoughLocation: {self!s}"

    @property
    def country_name(self) -> str:
        country = Country.from_alpha2(self.country_code)  # type: ignore[arg-type]
        if TYPE_CHECKING:
            # The code is validated
            assert country is not None

        return country.name

    @property
    def subdivision_name(self) -> str | None:
        if not self.subdivision_code:
            return None
        country = Country.from_alpha2(self.country_code)  # type: ignore[arg-type]
        if TYPE_CHECKING:
            # The code is validated
            assert country is not None
        return country.get_subdivision_name(self.subdivision_code)  # type: ignore[arg-type]
