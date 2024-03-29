from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("TT-ARI", "Arima"),
    Subdivision("TT-CHA", "Chaguanas"),
    Subdivision("TT-CTT", "Couva-Tabaquite-Talparo"),
    Subdivision("TT-DMN", "Diego Martin"),
    Subdivision("TT-MRC", "Mayaro-Rio Claro"),
    Subdivision("TT-PED", "Penal-Debe"),
    Subdivision("TT-POS", "Port of Spain"),
    Subdivision("TT-PRT", "Princes Town"),
    Subdivision("TT-PTF", "Point Fortin"),
    Subdivision("TT-SFO", "San Fernando"),
    Subdivision("TT-SGE", "Sangre Grande"),
    Subdivision("TT-SIP", "Siparia"),
    Subdivision("TT-SJL", "San Juan-Laventille"),
    Subdivision("TT-TOB", "Tobago"),
    Subdivision("TT-TUP", "Tunapuna-Piarco"),
]
