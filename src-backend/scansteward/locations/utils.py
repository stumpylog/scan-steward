from functools import lru_cache
from typing import TYPE_CHECKING

import pycountry
from pycountry import SubdivisionHierarchy


@lru_cache
def get_subdivision_name_by_code(country_code: str, subdivision_code: str) -> str | None:
    """
    Returns the name of the given subdivision code in the given country code, or None if the subdivision is not valid.
    """
    country_divisions = pycountry.subdivisions.get(country_code=country_code)  # type: ignore[assignment]
    if TYPE_CHECKING:
        country_divisions: set[SubdivisionHierarchy]
    for division in country_divisions:
        if division.code == subdivision_code:
            return division.name
    return None


@lru_cache
def get_country_short_name_by_code(country_code: str) -> str | None:
    """
    Returns the name of the given country code, or None if the country is not valid.
    """
    country = pycountry.countries.get(alpha_2=country_code)
    return country.name if country else None


@lru_cache
def get_country_code_from_name(country_name: str) -> str | None:
    """
    Returns the code of the given country name, or None if the country is not valid.
    """
    results = pycountry.countries.search_fuzzy(country_name)
    if TYPE_CHECKING:
        results: list[pycountry.ExistingCountries]
    if results:
        return results[0].alpha_2
    return None


@lru_cache
def get_subdivision_code_from_name(country_alpha2: str, subdivision_name: str) -> str | None:
    """
    Returns the code of the given country name, or None if the country is not valid.
    """
    if subdivision_name.lower() == "dc":
        subdivision_name = "District of Columbia"
    results = pycountry.subdivisions.search_fuzzy(subdivision_name)
    for result in results:
        if result.country_code == country_alpha2:
            return result.code
    return None
