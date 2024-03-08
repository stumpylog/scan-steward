from __future__ import annotations

from ninja import FilterSchema

from scansteward.common.schemas import TreeLikeSimpleNamedCreate
from scansteward.common.schemas import TreeLikeSimpleNamedRead
from scansteward.common.schemas import TreeLikeSimpleNamedTree
from scansteward.common.schemas import TreeLikeSimpleNamedUpdate


class TagCreate(TreeLikeSimpleNamedCreate):
    pass


class TagRead(TreeLikeSimpleNamedRead):
    pass


class TagTree(TreeLikeSimpleNamedTree):
    pass


class TagUpdate(TreeLikeSimpleNamedUpdate):
    pass


class TagNameFilter(FilterSchema):
    name: str | None = None
