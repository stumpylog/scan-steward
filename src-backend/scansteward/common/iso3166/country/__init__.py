from collections.abc import Generator
from functools import lru_cache

from scansteward.common.iso3166.models import Country


@lru_cache
def get_country_by_code(country_alpha_2: str) -> Country | None:
    """
    Get a country by its alpha-2 code.
    """
    from scansteward.common.iso3166.country.countries import ALPHA2_CODE_TO_COUNTRIES

    return ALPHA2_CODE_TO_COUNTRIES.get(country_alpha_2)


@lru_cache
def get_country_by_exact_name(country_name: str) -> Country | None:
    """
    Get a country by its exact name.
    """
    from scansteward.common.iso3166.country.countries import ALPHA2_CODE_TO_COUNTRIES

    for country_code in ALPHA2_CODE_TO_COUNTRIES:
        country = ALPHA2_CODE_TO_COUNTRIES[country_code]
        if country.name == country_name:
            return country
    return None


@lru_cache
def get_country_by_partial_name(
    country_name: str,
    *,
    ratio: float | int = 75.0,
) -> Generator[Country, None, None]:
    """
    Get a country by its partial name.
    """
    from rapidfuzz.fuzz import ratio as fuzz_ratio
    from rapidfuzz.utils import default_process

    from scansteward.common.iso3166.country.countries import ALPHA2_CODE_TO_COUNTRIES

    processed_name = default_process(country_name)

    for country_code in ALPHA2_CODE_TO_COUNTRIES:
        country = ALPHA2_CODE_TO_COUNTRIES[country_code]
        similarity = fuzz_ratio(processed_name, default_process(country.name))
        if similarity >= ratio:
            yield country


@lru_cache
def valid_country_code(country_alpha_2: str) -> bool:
    """
    Returns True if the given country code is valid, False otherwise.
    """

    from scansteward.common.iso3166.country.countries import ALPHA2_CODE_TO_COUNTRIES

    return country_alpha_2.upper() in ALPHA2_CODE_TO_COUNTRIES
