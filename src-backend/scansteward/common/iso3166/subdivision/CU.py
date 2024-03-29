from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CU-01", "Pinar del Río"),
    Subdivision("CU-03", "La Habana"),
    Subdivision("CU-04", "Matanzas"),
    Subdivision("CU-05", "Villa Clara"),
    Subdivision("CU-06", "Cienfuegos"),
    Subdivision("CU-07", "Sancti Spíritus"),
    Subdivision("CU-08", "Ciego de Ávila"),
    Subdivision("CU-09", "Camagüey"),
    Subdivision("CU-10", "Las Tunas"),
    Subdivision("CU-11", "Holguín"),
    Subdivision("CU-12", "Granma"),
    Subdivision("CU-13", "Santiago de Cuba"),
    Subdivision("CU-14", "Guantánamo"),
    Subdivision("CU-15", "Artemisa"),
    Subdivision("CU-16", "Mayabeque"),
    Subdivision("CU-99", "Isla de la Juventud"),
]
