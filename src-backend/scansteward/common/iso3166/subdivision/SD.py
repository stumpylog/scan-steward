from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SD-DC", "Central Darfur"),
    Subdivision("SD-DE", "East Darfur"),
    Subdivision("SD-DN", "North Darfur"),
    Subdivision("SD-DS", "South Darfur"),
    Subdivision("SD-DW", "West Darfur"),
    Subdivision("SD-GD", "Gedaref"),
    Subdivision("SD-GK", "West Kordofan"),
    Subdivision("SD-GZ", "Gezira"),
    Subdivision("SD-KA", "Kassala"),
    Subdivision("SD-KH", "Khartoum"),
    Subdivision("SD-KN", "North Kordofan"),
    Subdivision("SD-KS", "South Kordofan"),
    Subdivision("SD-NB", "Blue Nile"),
    Subdivision("SD-NO", "Northern"),
    Subdivision("SD-NR", "River Nile"),
    Subdivision("SD-NW", "White Nile"),
    Subdivision("SD-RS", "Red Sea"),
    Subdivision("SD-SI", "Sennar"),
]
