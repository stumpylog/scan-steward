from typing import Final

from scansteward.common.iso3166.models import Subdivision

SUBDIVISIONS: Final[list[Subdivision]] = [
    Subdivision("CL-AI", "Aisén del General Carlos Ibañez del Campo"),
    Subdivision("CL-AN", "Antofagasta"),
    Subdivision("CL-AP", "Arica y Parinacota"),
    Subdivision("CL-AR", "La Araucanía"),
    Subdivision("CL-AT", "Atacama"),
    Subdivision("CL-BI", "Biobío"),
    Subdivision("CL-CO", "Coquimbo"),
    Subdivision("CL-LI", "Libertador General Bernardo O'Higgins"),
    Subdivision("CL-LL", "Los Lagos"),
    Subdivision("CL-LR", "Los Ríos"),
    Subdivision("CL-MA", "Magallanes"),
    Subdivision("CL-ML", "Maule"),
    Subdivision("CL-NB", "Ñuble"),
    Subdivision("CL-RM", "Región Metropolitana de Santiago"),
    Subdivision("CL-TA", "Tarapacá"),
    Subdivision("CL-VS", "Valparaíso"),
]
