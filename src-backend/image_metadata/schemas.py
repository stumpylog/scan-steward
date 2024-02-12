from typing import ClassVar

from ninja import ModelSchema

from image_metadata.models import Subject


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
