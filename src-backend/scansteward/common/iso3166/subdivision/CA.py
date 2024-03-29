from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CA-AB", "Alberta"),
    Subdivision("CA-BC", "British Columbia"),
    Subdivision("CA-MB", "Manitoba"),
    Subdivision("CA-NB", "New Brunswick"),
    Subdivision("CA-NL", "Newfoundland and Labrador"),
    Subdivision("CA-NS", "Nova Scotia"),
    Subdivision("CA-NT", "Northwest Territories"),
    Subdivision("CA-NU", "Nunavut"),
    Subdivision("CA-ON", "Ontario"),
    Subdivision("CA-PE", "Prince Edward Island"),
    Subdivision("CA-QC", "Quebec"),
    Subdivision("CA-SK", "Saskatchewan"),
    Subdivision("CA-YT", "Yukon"),
]
