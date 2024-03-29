from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("MC-CL", "La Colle"),
    Subdivision("MC-CO", "La Condamine"),
    Subdivision("MC-FO", "Fontvieille"),
    Subdivision("MC-GA", "La Gare"),
    Subdivision("MC-JE", "Jardin Exotique"),
    Subdivision("MC-LA", "Larvotto"),
    Subdivision("MC-MA", "Malbousquet"),
    Subdivision("MC-MC", "Monte-Carlo"),
    Subdivision("MC-MG", "Moneghetti"),
    Subdivision("MC-MO", "Monaco-Ville"),
    Subdivision("MC-MU", "Moulins"),
    Subdivision("MC-PH", "Port-Hercule"),
    Subdivision("MC-SD", "Sainte-Dévote"),
    Subdivision("MC-SO", "La Source"),
    Subdivision("MC-SP", "Spélugues"),
    Subdivision("MC-SR", "Saint-Roman"),
    Subdivision("MC-VR", "Vallon de la Rousse"),
]
