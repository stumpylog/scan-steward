from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("AU-ACT", "Australian Capital Territory"),
    Subdivision("AU-NSW", "New South Wales"),
    Subdivision("AU-NT", "Northern Territory"),
    Subdivision("AU-QLD", "Queensland"),
    Subdivision("AU-SA", "South Australia"),
    Subdivision("AU-TAS", "Tasmania"),
    Subdivision("AU-VIC", "Victoria"),
    Subdivision("AU-WA", "Western Australia"),
]
