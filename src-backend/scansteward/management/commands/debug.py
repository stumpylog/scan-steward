from pathlib import Path

from django.core.management.base import BaseCommand

from scansteward.imageops.metadata import read_image_metadata
from scansteward.imageops.metadata import write_image_metadata


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        file = Path(__file__).parent.parent.parent / "tests" / "samples" / "images" / "sample1.jpg"
        assert file.exists()
        assert file.is_file()

        metadata = read_image_metadata(file)

        write_image_metadata(metadata)
