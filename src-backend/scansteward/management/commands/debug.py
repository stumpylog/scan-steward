from django.core.management.base import BaseCommand
from iso3166_2 import ISO3166_2


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        max_length = 0
        iso = ISO3166_2()
        for country in iso.subdivision_codes():
            for region in iso[country]:
                if len(region) > max_length:
                    max_length = len(region)
