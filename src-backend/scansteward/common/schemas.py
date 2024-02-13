from __future__ import annotations

from ninja import Schema


class SimpleNamedSchema(Schema):
    """
    Common schema for the SimpleNamedModel abstract model
    """

    name: str
    description: str | None = None
    parent_id: int | None = None


class SimpleNamedWithIdSchema(SimpleNamedSchema):
    """
    Common schema for the SimpleNamedModel abstract model including its id
    """

    id: int


class TreeLikeSimpleNamedCreate(SimpleNamedSchema):
    """
    Common schema for creating a tree like entry
    """


class TreeLikeSimpleNamedRead(SimpleNamedWithIdSchema):
    """
    Common schema for reading a tree like entry
    """

    id: int


class TreeLikeSimpleNamedTree(SimpleNamedWithIdSchema):
    """
    Common schema for reading the Tree
    """

    children: list[TreeLikeSimpleNamedTree] | None = None


TreeLikeSimpleNamedTree.model_rebuild()


class TreeLikeSimpleNamedUpdate(Schema):
    """
    Common schema for updating a tree like entry
    """

    name: str | None = None
    description: str | None = None
    parent_id: int | None = None
