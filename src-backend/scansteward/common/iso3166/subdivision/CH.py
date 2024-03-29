from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CH-AG", "Aargau"),
    Subdivision("CH-AI", "Appenzell Innerrhoden"),
    Subdivision("CH-AR", "Appenzell Ausserrhoden"),
    Subdivision("CH-BE", "Berne"),
    Subdivision("CH-BL", "Basel-Landschaft"),
    Subdivision("CH-BS", "Basel-Stadt"),
    Subdivision("CH-FR", "Fribourg"),
    Subdivision("CH-GE", "Genève"),
    Subdivision("CH-GL", "Glarus"),
    Subdivision("CH-GR", "Graubünden"),
    Subdivision("CH-JU", "Jura"),
    Subdivision("CH-LU", "Luzern"),
    Subdivision("CH-NE", "Neuchâtel"),
    Subdivision("CH-NW", "Nidwalden"),
    Subdivision("CH-OW", "Obwalden"),
    Subdivision("CH-SG", "Sankt Gallen"),
    Subdivision("CH-SH", "Schaffhausen"),
    Subdivision("CH-SO", "Solothurn"),
    Subdivision("CH-SZ", "Schwyz"),
    Subdivision("CH-TG", "Thurgau"),
    Subdivision("CH-TI", "Ticino"),
    Subdivision("CH-UR", "Uri"),
    Subdivision("CH-VD", "Vaud"),
    Subdivision("CH-VS", "Valais"),
    Subdivision("CH-ZG", "Zug"),
    Subdivision("CH-ZH", "Zürich"),
]
