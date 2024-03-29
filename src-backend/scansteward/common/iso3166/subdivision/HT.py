from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("HT-AR", "Artibonite"),
    Subdivision("HT-CE", "Centre"),
    Subdivision("HT-GA", "Grande’Anse"),
    Subdivision("HT-ND", "Nord"),
    Subdivision("HT-NE", "Nord-Est"),
    Subdivision("HT-NI", "Nippes"),
    Subdivision("HT-NO", "Nord-Ouest"),
    Subdivision("HT-OU", "Ouest"),
    Subdivision("HT-SD", "Sud"),
    Subdivision("HT-SE", "Sud-Est"),
]
