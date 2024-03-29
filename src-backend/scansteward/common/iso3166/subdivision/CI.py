from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CI-AB", "Abidjan"),
    Subdivision("CI-BS", "Bas-Sassandra"),
    Subdivision("CI-CM", "Comoé"),
    Subdivision("CI-DN", "Denguélé"),
    Subdivision("CI-GD", "Gôh-Djiboua"),
    Subdivision("CI-LC", "Lacs"),
    Subdivision("CI-LG", "Lagunes"),
    Subdivision("CI-MG", "Montagnes"),
    Subdivision("CI-SM", "Sassandra-Marahoué"),
    Subdivision("CI-SV", "Savanes"),
    Subdivision("CI-VB", "Vallée du Bandama"),
    Subdivision("CI-WR", "Woroba"),
    Subdivision("CI-YM", "Yamoussoukro"),
    Subdivision("CI-ZZ", "Zanzan"),
]
