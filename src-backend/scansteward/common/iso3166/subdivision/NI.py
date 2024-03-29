from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("NI-AN", "Costa Caribe Norte"),
    Subdivision("NI-AS", "Costa Caribe Sur"),
    Subdivision("NI-BO", "Boaco"),
    Subdivision("NI-CA", "Carazo"),
    Subdivision("NI-CI", "Chinandega"),
    Subdivision("NI-CO", "Chontales"),
    Subdivision("NI-ES", "Estelí"),
    Subdivision("NI-GR", "Granada"),
    Subdivision("NI-JI", "Jinotega"),
    Subdivision("NI-LE", "León"),
    Subdivision("NI-MD", "Madriz"),
    Subdivision("NI-MN", "Managua"),
    Subdivision("NI-MS", "Masaya"),
    Subdivision("NI-MT", "Matagalpa"),
    Subdivision("NI-NS", "Nueva Segovia"),
    Subdivision("NI-RI", "Rivas"),
    Subdivision("NI-SJ", "Río San Juan"),
]
