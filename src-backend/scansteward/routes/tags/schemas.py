from __future__ import annotations

import sys

from ninja import FilterSchema
from ninja import Schema
from pydantic import model_validator

if sys.version_info > (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class TagCreate(Schema):
    name: str
    description: str | None = None
    parent_id: int | None = None


class TagRead(Schema):
    id: int
    name: str
    applied: bool
    description: str | None = None
    parent_id: int | None = None


class TagTree(Schema):
    id: int
    name: str
    applied: bool
    description: str | None = None
    parent_id: int | None = None
    children: list[TagTree] | None = None


TagTree.model_rebuild()


class TagUpdate(Schema):
    name: str | None = None
    description: str | None = None
    parent_id: int | None = None

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> Self:
        if not (self.name or self.description or self.parent_id):
            raise ValueError("At least one field must be updated.")  # noqa: TRY003, EM101
        return self


class TagNameFilter(FilterSchema):
    name: str | None = None
