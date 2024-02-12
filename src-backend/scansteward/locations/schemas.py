from __future__ import annotations

from ninja import Schema


class LocationCreate(Schema):
    name: str
    description: str | None = None
    parent_id: int | None = None


class LocationRead(Schema):
    id: int
    name: str
    description: str | None = None
    parent_id: int | None = None


LocationRead.model_rebuild()


class LocationTree(Schema):
    id: int
    name: str
    description: str | None = None
    children: list[LocationTree] | None = None


LocationTree.model_rebuild()


class LocationUpdate(Schema):
    id: int
    name: str
    description: str | None = None
    parent_id: int | None = None
