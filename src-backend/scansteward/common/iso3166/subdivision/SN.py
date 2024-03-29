from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SN-DB", "Diourbel"),
    Subdivision("SN-DK", "Dakar"),
    Subdivision("SN-FK", "Fatick"),
    Subdivision("SN-KA", "Kaffrine"),
    Subdivision("SN-KD", "Kolda"),
    Subdivision("SN-KE", "Kédougou"),
    Subdivision("SN-KL", "Kaolack"),
    Subdivision("SN-LG", "Louga"),
    Subdivision("SN-MT", "Matam"),
    Subdivision("SN-SE", "Sédhiou"),
    Subdivision("SN-SL", "Saint-Louis"),
    Subdivision("SN-TC", "Tambacounda"),
    Subdivision("SN-TH", "Thiès"),
    Subdivision("SN-ZG", "Ziguinchor"),
]
