from typing import ClassVar

from ninja import ModelSchema

from image_metadata.models import Location
from image_metadata.models import Person
from image_metadata.models import Subject


class LocationIn(ModelSchema):
    class Meta:
        model = Location
        fields: ClassVar[list[str]] = [
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class LocationOut(ModelSchema):
    class Meta:
        model = Location
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]


class LocationUpdate(ModelSchema):
    class Meta:
        model = Location
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class SubjectIn(ModelSchema):
    class Meta:
        model = Subject
        fields: ClassVar[list[str]] = [
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class SubjectOut(ModelSchema):
    class Meta:
        model = Subject
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]


class SubjectUpdate(ModelSchema):
    class Meta:
        model = Subject
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class PersonIn(ModelSchema):
    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class PersonOut(ModelSchema):
    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]


class PersonUpdate(ModelSchema):
    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]
