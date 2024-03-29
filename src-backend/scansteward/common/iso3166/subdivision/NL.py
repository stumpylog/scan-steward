from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("NL-AW", "Aruba"),
    Subdivision("NL-BQ1", "Bonaire"),
    Subdivision("NL-BQ2", "Saba"),
    Subdivision("NL-BQ3", "Sint Eustatius"),
    Subdivision("NL-CW", "Curaçao"),
    Subdivision("NL-DR", "Drenthe"),
    Subdivision("NL-FL", "Flevoland"),
    Subdivision("NL-FR", "Fryslân"),
    Subdivision("NL-GE", "Gelderland"),
    Subdivision("NL-GR", "Groningen"),
    Subdivision("NL-LI", "Limburg"),
    Subdivision("NL-NB", "Noord-Brabant"),
    Subdivision("NL-NH", "Noord-Holland"),
    Subdivision("NL-OV", "Overijssel"),
    Subdivision("NL-SX", "Sint Maarten"),
    Subdivision("NL-UT", "Utrecht"),
    Subdivision("NL-ZE", "Zeeland"),
    Subdivision("NL-ZH", "Zuid-Holland"),
]
