import importlib
from functools import lru_cache
from pathlib import Path

from scansteward.common.iso3166.models import Subdivision


def get_subdivisions_by_country_code(country_alpha_2: str) -> list[Subdivision]:
    """
    Returns a list of subdivisions for the given country code.

    The list is loaded dynamically from the appropriate package
    """
    module = importlib.import_module(f".{country_alpha_2}", package=__name__)
    return module.SUBDIVISIONS


@lru_cache
def valid_subdivision_code(subdivision_code: str) -> bool:
    """
    Returns True if the given code is a valid subdivision code, otherwise False.
    """
    if "-" not in subdivision_code:
        return False
    country_code = subdivision_code.split("-")[0].upper()
    module_path = Path(__file__).parent / f"{country_code}.py"
    if not module_path.exists():
        return False
    module = importlib.import_module(f".{country_code}", package=__name__)
    subdivision_codes: str[str] = {subdivision.code for subdivision in module.SUBDIVISIONS}
    return subdivision_code in subdivision_codes
