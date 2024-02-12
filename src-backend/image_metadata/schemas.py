from typing import ClassVar

from ninja import ModelSchema

from image_metadata.models import Tag


class TagIn(ModelSchema):
    class Meta:
        model = Tag
        fields: ClassVar[list[str]] = [
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]


class TagOut(ModelSchema):
    class Meta:
        model = Tag
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]


class TagUpdate(ModelSchema):
    class Meta:
        model = Tag
        fields: ClassVar[list[str]] = [
            "id",
            "name",
            "description",
        ]
        fields_optional: ClassVar[list[str]] = ["description"]
