from functools import lru_cache
from typing import TYPE_CHECKING

import pycountry
from pycountry import SubdivisionHierarchy


@lru_cache
def subdivision_in_country(country_code: str, subdivision_code: str) -> bool:
    """
    Returns True if the given country code and subdivision code are valid together.
    """

    country_divisions = pycountry.subdivisions.get(country_code=country_code)  # type: ignore[assignment]
    if TYPE_CHECKING:
        country_divisions: set[SubdivisionHierarchy]
    return any(division.code == subdivision_code for division in country_divisions)
