from pathlib import Path

from django.core.management.base import BaseCommand

from scansteward.imageops.models import ImageMetadata
from scansteward.imageops.models import RotationEnum
from scansteward.imageops.orientation import bulk_write_image_rotation
from scansteward.imageops.orientation import read_image_rotation


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        image = Path(r"deck5-0011.jpg")
        rotation = read_image_rotation(image)

        bulk_write_image_rotation([ImageMetadata(SourceFile=image, Orientation=RotationEnum.ROTATE_180)])
