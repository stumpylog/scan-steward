from functools import lru_cache

from scansteward.common.iso3166.country import get_country_by_code
from scansteward.common.iso3166.country import get_country_by_partial_name


@lru_cache
def subdivision_in_country(country_code: str, subdivision_code: str) -> bool:
    """
    Returns True if the given country code and subdivision code are valid together.
    """
    country = get_country_by_code(country_code)
    if not country:
        return False
    return country.contains_subdivision(subdivision_code)


@lru_cache
def get_country_code_from_name(country_name: str) -> str | None:
    """
    Returns the code of the given country name, or None if the country is not valid.
    """
    if country_name in {"US", "USA"}:
        country_name = "United States"
    results = list(get_country_by_partial_name(country_name))
    if results:
        return results[0].alpha2
    return None


@lru_cache
def get_subdivision_code_from_name(
    country_alpha2: str,
    subdivision_name: str,
) -> str | None:
    """
    Returns the code of the given country name, or None if the country is not valid.
    """
    if subdivision_name.lower() == "dc":
        subdivision_name = "District of Columbia"
    country = get_country_by_code(country_alpha2)
    if not country:
        return None
    for subdivision in country.subdivisions:
        if subdivision.name == subdivision_name:
            return subdivision.code
    return None
