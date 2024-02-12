from typing import ClassVar

from ninja import ModelSchema

from scansteward.models import Person


class PersonCreate(ModelSchema):
    """
    Schema to create a Person
    """

    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class PersonRead(ModelSchema):
    """
    Schema when reading a person
    """

    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]


class PersonUpdate(ModelSchema):
    """
    Schema to update a person
    """

    class Meta:
        model = Person
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]
