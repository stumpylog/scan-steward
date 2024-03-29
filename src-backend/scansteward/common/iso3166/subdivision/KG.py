from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("KG-B", "Batken"),
    Subdivision("KG-C", "Chuyskaya oblast'"),
    Subdivision("KG-GB", "Bishkek Shaary"),
    Subdivision("KG-GO", "Gorod Osh"),
    Subdivision("KG-J", "Dzhalal-Abadskaya oblast'"),
    Subdivision("KG-N", "Naryn"),
    Subdivision("KG-O", "Osh"),
    Subdivision("KG-T", "Talas"),
    Subdivision("KG-Y", "Issyk-Kul'skaja oblast'"),
]
