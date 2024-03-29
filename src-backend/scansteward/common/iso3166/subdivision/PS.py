from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("PS-BTH", "Bethlehem"),
    Subdivision("PS-DEB", "Deir El Balah"),
    Subdivision("PS-GZA", "Gaza"),
    Subdivision("PS-HBN", "Hebron"),
    Subdivision("PS-JEM", "Jerusalem"),
    Subdivision("PS-JEN", "Jenin"),
    Subdivision("PS-JRH", "Jericho and Al Aghwar"),
    Subdivision("PS-KYS", "Khan Yunis"),
    Subdivision("PS-NBS", "Nablus"),
    Subdivision("PS-NGZ", "North Gaza"),
    Subdivision("PS-QQA", "Qalqilya"),
    Subdivision("PS-RBH", "Ramallah"),
    Subdivision("PS-RFH", "Rafah"),
    Subdivision("PS-SLT", "Salfit"),
    Subdivision("PS-TBS", "Tubas"),
    Subdivision("PS-TKM", "Tulkarm"),
]
