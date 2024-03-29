from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("NO-03", "Oslo"),
    Subdivision("NO-11", "Rogaland"),
    Subdivision("NO-15", "Møre og Romsdal"),
    Subdivision("NO-18", "Nordland"),
    Subdivision("NO-21", "Svalbard (Arctic Region)"),
    Subdivision("NO-22", "Jan Mayen (Arctic Region)"),
    Subdivision("NO-30", "Viken"),
    Subdivision("NO-34", "Innlandet"),
    Subdivision("NO-38", "Vestfold og Telemark"),
    Subdivision("NO-42", "Agder"),
    Subdivision("NO-46", "Vestland"),
    Subdivision("NO-50", "Trööndelage"),
    Subdivision("NO-54", "Romssa ja Finnmárkku"),
]
