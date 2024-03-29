from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("TD-BA", "Batha"),
    Subdivision("TD-BG", "Bahr el Ghazal"),
    Subdivision("TD-BO", "Borkou"),
    Subdivision("TD-CB", "Chari-Baguirmi"),
    Subdivision("TD-EE", "Ennedi-Est"),
    Subdivision("TD-EO", "Ennedi-Ouest"),
    Subdivision("TD-GR", "Guéra"),
    Subdivision("TD-HL", "Hadjer Lamis"),
    Subdivision("TD-KA", "Kanem"),
    Subdivision("TD-LC", "Lac"),
    Subdivision("TD-LO", "Logone-Occidental"),
    Subdivision("TD-LR", "Logone-Oriental"),
    Subdivision("TD-MA", "Mandoul"),
    Subdivision("TD-MC", "Moyen-Chari"),
    Subdivision("TD-ME", "Mayo-Kebbi-Est"),
    Subdivision("TD-MO", "Mayo-Kebbi-Ouest"),
    Subdivision("TD-ND", "Ville de Ndjamena"),
    Subdivision("TD-OD", "Ouaddaï"),
    Subdivision("TD-SA", "Salamat"),
    Subdivision("TD-SI", "Sila"),
    Subdivision("TD-TA", "Tandjilé"),
    Subdivision("TD-TI", "Tibesti"),
    Subdivision("TD-WF", "Wadi Fira"),
]
