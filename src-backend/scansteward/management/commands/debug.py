from pathlib import Path

from django.core.management.base import BaseCommand

from scansteward.imageops.keywords import read_keywords
from scansteward.imageops.keywords import set_keywords
from scansteward.imageops.faces import read_face_structs, write_face_structs


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        image = Path(r"deck5-0011.jpg")
        faces = read_face_structs(image)

        from pprint import pprint

        pprint(faces)
