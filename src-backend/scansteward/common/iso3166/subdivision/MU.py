from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MU-AG", "Agalega Islands"),
    Subdivision("MU-BL", "Black River"),
    Subdivision("MU-CC", "Cargados Carajos Shoals"),
    Subdivision("MU-FL", "Flacq"),
    Subdivision("MU-GP", "Grand Port"),
    Subdivision("MU-MO", "Moka"),
    Subdivision("MU-PA", "Pamplemousses"),
    Subdivision("MU-PL", "Port Louis"),
    Subdivision("MU-PW", "Plaines Wilhems"),
    Subdivision("MU-RO", "Rodrigues Island"),
    Subdivision("MU-RR", "Rivière du Rempart"),
    Subdivision("MU-SA", "Savanne"),
]
