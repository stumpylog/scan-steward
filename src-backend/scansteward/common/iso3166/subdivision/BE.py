from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("BE-BRU", "Bruxelles-Capitale, Région de"),
    Subdivision("BE-VAN", "Antwerpen"),
    Subdivision("BE-VBR", "Vlaams-Brabant"),
    Subdivision("BE-VLG", "Vlaams Gewest"),
    Subdivision("BE-VLI", "Limburg"),
    Subdivision("BE-VOV", "Oost-Vlaanderen"),
    Subdivision("BE-VWV", "West-Vlaanderen"),
    Subdivision("BE-WAL", "wallonne, Région"),
    Subdivision("BE-WBR", "Brabant wallon"),
    Subdivision("BE-WHT", "Hainaut"),
    Subdivision("BE-WLG", "Liège"),
    Subdivision("BE-WLX", "Luxembourg"),
    Subdivision("BE-WNA", "Namur"),
]
