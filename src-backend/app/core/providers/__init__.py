from litestar.params import Parameter
from litestar.repository.filters import LimitOffset


async def provide_limit_offset_pagination(
    offset: int = Parameter(ge=1, query="offset", default=1, required=False),
    limit: int = Parameter(
        query="limit",
        ge=1,
        default=10,
        required=False,
    ),
) -> LimitOffset:
    """
    Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    limit : int
        LIMIT to apply to select.
    offset : int
        OFFSET to apply to select.
    """
    return LimitOffset(limit, limit * (offset - 1))
