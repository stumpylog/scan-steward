from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("ET-AA", "Addis Ababa"),
    Subdivision("ET-AF", "Afar"),
    Subdivision("ET-AM", "Amara"),
    Subdivision("ET-BE", "Benshangul-Gumaz"),
    Subdivision("ET-DD", "Dire Dawa"),
    Subdivision("ET-GA", "Gambela Peoples"),
    Subdivision("ET-HA", "Harari People"),
    Subdivision("ET-OR", "Oromia"),
    Subdivision("ET-SI", "Sidama"),
    Subdivision("ET-SN", "Southern Nations, Nationalities and Peoples"),
    Subdivision("ET-SO", "Somali"),
    Subdivision("ET-SW", "Southwest Ethiopia Peoples"),
    Subdivision("ET-TI", "Tigrai"),
]
