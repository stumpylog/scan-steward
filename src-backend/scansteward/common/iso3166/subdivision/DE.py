from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("DE-BB", "Brandenburg"),
    Subdivision("DE-BE", "Berlin"),
    Subdivision("DE-BW", "Baden-Württemberg"),
    Subdivision("DE-BY", "Bayern"),
    Subdivision("DE-HB", "Bremen"),
    Subdivision("DE-HE", "Hessen"),
    Subdivision("DE-HH", "Hamburg"),
    Subdivision("DE-MV", "Mecklenburg-Vorpommern"),
    Subdivision("DE-NI", "Niedersachsen"),
    Subdivision("DE-NW", "Nordrhein-Westfalen"),
    Subdivision("DE-RP", "Rheinland-Pfalz"),
    Subdivision("DE-SH", "Schleswig-Holstein"),
    Subdivision("DE-SL", "Saarland"),
    Subdivision("DE-SN", "Sachsen"),
    Subdivision("DE-ST", "Sachsen-Anhalt"),
    Subdivision("DE-TH", "Thüringen"),
]
