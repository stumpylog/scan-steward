from pathlib import Path

from django.core.management.base import BaseCommand

from scansteward.imageops.keywords import read_keywords


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        image = Path(r"D:\Pictures\Scans\Parents'\In_Work\deck5-0011.jpg")
        kwrds = read_keywords(image)

        print(kwrds[5]["1975"])
