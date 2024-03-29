from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PT-01", "Aveiro"),
    Subdivision("PT-02", "Beja"),
    Subdivision("PT-03", "Braga"),
    Subdivision("PT-04", "Bragança"),
    Subdivision("PT-05", "Castelo Branco"),
    Subdivision("PT-06", "Coimbra"),
    Subdivision("PT-07", "Évora"),
    Subdivision("PT-08", "Faro"),
    Subdivision("PT-09", "Guarda"),
    Subdivision("PT-10", "Leiria"),
    Subdivision("PT-11", "Lisboa"),
    Subdivision("PT-12", "Portalegre"),
    Subdivision("PT-13", "Porto"),
    Subdivision("PT-14", "Santarém"),
    Subdivision("PT-15", "Setúbal"),
    Subdivision("PT-16", "Viana do Castelo"),
    Subdivision("PT-17", "Vila Real"),
    Subdivision("PT-18", "Viseu"),
    Subdivision("PT-20", "Região Autónoma dos Açores"),
    Subdivision("PT-30", "Região Autónoma da Madeira"),
]
