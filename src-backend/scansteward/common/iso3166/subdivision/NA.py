from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("NA-CA", "Zambezi"),
    Subdivision("NA-ER", "Erongo"),
    Subdivision("NA-HA", "Hardap"),
    Subdivision("NA-KA", "//Karas"),
    Subdivision("NA-KE", "Kavango East"),
    Subdivision("NA-KH", "Khomas"),
    Subdivision("NA-KU", "Kunene"),
    Subdivision("NA-KW", "Kavango West"),
    Subdivision("NA-OD", "Otjozondjupa"),
    Subdivision("NA-OH", "Omaheke"),
    Subdivision("NA-ON", "Oshana"),
    Subdivision("NA-OS", "Omusati"),
    Subdivision("NA-OT", "Oshikoto"),
    Subdivision("NA-OW", "Ohangwena"),
]
