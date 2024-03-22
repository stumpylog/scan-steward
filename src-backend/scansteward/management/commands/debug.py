from django.core.management.base import BaseCommand
from iso3166_2 import ISO3166_2


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        max_length = 0
        max_name = None
        max_country = None
        iso = ISO3166_2()
        for country in iso.subdivision_codes():
            print(country)
            for region in iso[country]:
                print(region)
                if len(region) > max_length:
                    max_name = region
                    max_country = country
                    max_length = len(region)
        print(max_country)
        print(max_length)
        print(max_name)
