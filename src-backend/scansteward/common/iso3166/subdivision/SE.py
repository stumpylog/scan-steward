from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("SE-AB", "Stockholms län [SE-01]"),
    Subdivision("SE-AC", "Västerbottens län [SE-24]"),
    Subdivision("SE-BD", "Norrbottens län [SE-25]"),
    Subdivision("SE-C", "Uppsala län [SE-03]"),
    Subdivision("SE-D", "Södermanlands län [SE-04]"),
    Subdivision("SE-E", "Östergötlands län [SE-05]"),
    Subdivision("SE-F", "Jönköpings län [SE-06]"),
    Subdivision("SE-G", "Kronobergs län [SE-07]"),
    Subdivision("SE-H", "Kalmar län [SE-08]"),
    Subdivision("SE-I", "Gotlands län [SE-09]"),
    Subdivision("SE-K", "Blekinge län [SE-10]"),
    Subdivision("SE-M", "Skåne län [SE-12]"),
    Subdivision("SE-N", "Hallands län [SE-13]"),
    Subdivision("SE-O", "Västra Götalands län [SE-14]"),
    Subdivision("SE-S", "Värmlands län [SE-17]"),
    Subdivision("SE-T", "Örebro län [SE-18]"),
    Subdivision("SE-U", "Västmanlands län [SE-19]"),
    Subdivision("SE-W", "Dalarnas län [SE-20]"),
    Subdivision("SE-X", "Gävleborgs län [SE-21]"),
    Subdivision("SE-Y", "Västernorrlands län [SE-22]"),
    Subdivision("SE-Z", "Jämtlands län [SE-23]"),
]
