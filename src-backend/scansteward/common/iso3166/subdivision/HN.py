from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("HN-AT", "Atlántida"),
    Subdivision("HN-CH", "Choluteca"),
    Subdivision("HN-CL", "Colón"),
    Subdivision("HN-CM", "Comayagua"),
    Subdivision("HN-CP", "Copán"),
    Subdivision("HN-CR", "Cortés"),
    Subdivision("HN-EP", "El Paraíso"),
    Subdivision("HN-FM", "Francisco Morazán"),
    Subdivision("HN-GD", "Gracias a Dios"),
    Subdivision("HN-IB", "Islas de la Bahía"),
    Subdivision("HN-IN", "Intibucá"),
    Subdivision("HN-LE", "Lempira"),
    Subdivision("HN-LP", "La Paz"),
    Subdivision("HN-OC", "Ocotepeque"),
    Subdivision("HN-OL", "Olancho"),
    Subdivision("HN-SB", "Santa Bárbara"),
    Subdivision("HN-VA", "Valle"),
    Subdivision("HN-YO", "Yoro"),
]
