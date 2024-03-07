from pathlib import Path
from pprint import pprint

from django.core.management.base import BaseCommand

from scansteward.imageops.keywords import read_keywords
from scansteward.imageops.keywords import write_keywords
from scansteward.imageops.models import KeywordStruct


class Command(BaseCommand):
    help = "Debug command to do stuff"

    def handle(self, *args, **options) -> None:
        image = Path(r"deck5-0011.jpg")
        metadata = read_keywords(image)
        pprint(metadata.model_dump())
        assert metadata.KeywordInfo is not None
        metadata.KeywordInfo.Hierarchy.append(
            KeywordStruct(
                Keyword="This is a new root",
                Children=[
                    KeywordStruct(
                        Keyword="This is below the new root",
                        Children=[KeywordStruct(Keyword="This is a test")],
                    ),
                ],
            ),
        )
        write_keywords(metadata)

        # bulk_write_image_rotation([ImageMetadata(SourceFile=image, Orientation=RotationEnum.ROTATE_180)])
